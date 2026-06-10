import numpy as np
import matplotlib.pyplot as plt

##############################
# Algorithms
##############################


def sample_discrete(prob_matrix: np.ndarray) -> np.ndarray:
    """
    Helper function to sample from discrete distributions row-wise.
    
    :param prob_matrix: 2D array where each row is a normalized probability distribution.
    :type prob_matrix: np.ndarray
    :return: 1D array of sampled indices.
    :rtype: np.ndarray
    """
    # Vectorized sampling using cumulative distribution per row
    cdf = np.cumsum(prob_matrix, axis=1)
    r = np.random.rand(prob_matrix.shape[0], 1)
    return np.sum(r > cdf, axis=1)


def generate_hmm_data(
    initial_dist: np.ndarray, 
    transition_matrix: np.ndarray, 
    emission_matrix: np.ndarray, 
    sim_length: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate true hidden states and observed emissions from a Hidden Markov Model.

    :param initial_dist: Initial state probability distribution, shape (num_states,).
    :type initial_dist: np.ndarray
    :param transition_matrix: Transition probability matrix T, shape (num_states, num_states).
    :type transition_matrix: np.ndarray
    :param emission_matrix: Emission probability matrix L, shape (num_states, num_obs_types).
    :type emission_matrix: np.ndarray
    :param sim_length: The length of the simulation sequence to generate.
    :type sim_length: int
    :return: A tuple containing (true_states, observations).
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    states = np.zeros(sim_length, dtype=int)
    observations = np.zeros(sim_length, dtype=int)
    
    states[0] = sample_discrete(initial_dist.reshape(1, -1))[0]
    observations[0] = sample_discrete(emission_matrix[states[0], :].reshape(1, -1))[0]
    
    for t in range(1, sim_length):
        states[t] = sample_discrete(transition_matrix[states[t-1], :].reshape(1, -1))[0]
        observations[t] = sample_discrete(emission_matrix[states[t], :].reshape(1, -1))[0]
        
    return states, observations

def generate_continuous_hmm_data(
    alpha_param: float, 
    sim_length: int, 
    sigma_x: float = 1.0, 
    sigma_y: float = 3.0
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate true hidden states and observed emissions for a continuous Gaussian HMM.
    
    :param alpha_param: Autoregressive coefficient for state transition.
    :param sim_length: Length of the simulation sequence.
    :param sigma_x: Standard deviation of the process noise (sqrt(1) = 1.0).
    :param sigma_y: Standard deviation of the observation noise (sqrt(9) = 3.0).
    :return: Tuple of (true_states, observations), shapes: (sim_length,), (sim_length,)
    """
    states = np.zeros(sim_length)
    observations = np.zeros(sim_length)
    
    # t = 0: Załóżmy start z rozkładu stacjonarnego lub po prostu z N(0, sigma_x^2)
    states[0] = np.random.normal(0, sigma_x)
    observations[0] = np.random.normal(states[0], sigma_y)
    
    for t in range(1, sim_length):
        states[t] = np.random.normal(alpha_param * states[t-1], sigma_x)
        observations[t] = np.random.normal(states[t], sigma_y)
        
    return states, observations

def forward_filtering_backward_sampling(
    initial_dist: np.ndarray, 
    transition_matrix: np.ndarray, 
    emission_matrix: np.ndarray, 
    observations: np.ndarray, 
    num_samples: int
) -> np.ndarray:
    """
    Perform Forward Filtering Backward Sampling (FFBS) to draw exact trajectory samples.

    :param initial_dist: Initial state probability distribution, shape (num_states,).
    :type initial_dist: np.ndarray
    :param transition_matrix: Transition probability matrix T, shape (num_states, num_states).
    :type transition_matrix: np.ndarray
    :param emission_matrix: Emission probability matrix L, shape (num_states, num_obs_types).
    :type emission_matrix: np.ndarray
    :param observations: Array of observed emission indices, shape (simulation_length,).
    :type observations: np.ndarray
    :param num_samples: Number of exact trajectory samples to generate.
    :type num_samples: int
    :return: Sampled state trajectories, shape (num_samples, simulation_length).
    :rtype: np.ndarray
    """
    num_states = transition_matrix.shape[0]
    sim_length = len(observations)
    
    # Forward Filtering: Store alpha scaled values to prevent underflow
    alpha = np.zeros((sim_length, num_states))
    
    # Step 0: Initialize
    alpha[0, :] = initial_dist * emission_matrix[:, observations[0]]
    alpha[0, :] /= np.sum(alpha[0, :])
    
    # Step 1: Forward recursion
    for t in range(1, sim_length):
        alpha[t, :] = (alpha[t-1, :] @ transition_matrix) * emission_matrix[:, observations[t]]
        alpha[t, :] /= np.sum(alpha[t, :])
    
    # if num_samples == 0 return alphas for reconstruction of betas  
    if num_samples == 0:
        return alpha
        
    # Backward Sampling
    sampled_trajectories = np.zeros((num_samples, sim_length), dtype=int)
    
    # Sample final state X_k from alpha[k]
    prob_k = np.tile(alpha[-1, :], (num_samples, 1))
    sampled_trajectories[:, -1] = sample_discrete(prob_k)
    
    # Recursive backward step
    for t in range(sim_length - 2, -1, -1):
        next_states = sampled_trajectories[:, t+1]
        
        # Calculate transition back: B_t proportional to alpha_t(x_t) * T(x_t, x_{t+1})
        # Vectorized over all parallel samples
        b_t = alpha[t, :, np.newaxis] * transition_matrix[:, next_states]  # shape (num_states, num_samples)
        b_t = b_t.T  # shape (num_samples, num_states)
        b_t /= np.sum(b_t, axis=1, keepdims=True)
        
        sampled_trajectories[:, t] = sample_discrete(b_t)
        
    return sampled_trajectories

def particle_filter_sis_pfs(
    initial_dist: np.ndarray, 
    initial_weights: np.ndarray,
    transition_matrix: np.ndarray, 
    emission_matrix: np.ndarray, 
    observations: np.ndarray, 
    num_particles: int,
    use_resampling: bool = True
) -> np.ndarray:
    """
    Sequential Importance Sampling (SIS) and Particle Filter (PF) with Multinomial Resampling.

    :param initial_dist: Initial state probability distribution, shape (num_states,).
    :type initial_dist: np.ndarray
    :param transition_matrix: Transition probability matrix T, shape (num_states, num_states).
    :type transition_matrix: np.ndarray
    :param emission_matrix: Emission probability matrix L, shape (num_states, num_obs_types).
    :type emission_matrix: np.ndarray
    :param observations: Array of observed emission indices, shape (simulation_length,).
    :type observations: np.ndarray
    :param num_particles: Number of particles (samples) used to approximate the distribution.
    :type num_particles: int
    :param use_resampling: If True, executes Particle Filter (SMC). If False, executes pure SIS.
    :type use_resampling: bool
    :return: Trajectories of all particles, shape (num_particles, simulation_length).
    :rtype: np.ndarray
    """
    num_states = transition_matrix.shape[0]
    sim_length = len(observations)
    
    # Store full trajectory history for all particles
    particles = np.zeros((num_particles, sim_length), dtype=int)
    empirical_dists = np.zeros((sim_length, num_states))
    
    weights = initial_weights.copy() / np.sum(initial_weights)
    
    # Step 0: Initialization
    prob_init = np.tile(initial_dist, (num_particles, 1))
    particles[:, 0] = sample_discrete(prob_init)
    weights *= emission_matrix[particles[:, 0], observations[0]]
    weights /= np.sum(weights)
    
    # calculate empirical distributions 
    for s in range(num_states):
        empirical_dists[0, s] = np.sum(weights[particles[:, 0] == s])

    # Sequential processing over time
    for t in range(1, sim_length):
        if use_resampling:
            # Resampling step (Multinomial selection based on current weights)
            prob_resample = np.tile(weights, (num_particles, 1))
            resample_idx = sample_discrete(prob_resample)
            
            # Reset particles trajectories and equalize weights
            particles = particles[resample_idx, :]
            weights = np.ones(num_particles) / num_particles
            
        # Transition step: Propagate particles using transition matrix T
        prob_trans = transition_matrix[particles[:, t-1], :]
        particles[:, t] = sample_discrete(prob_trans)
        
        # Weight update step based on likelihood of current observation
        weights *= emission_matrix[particles[:, t], observations[t]]
        
        # Normalize weights to prevent numerical collapse
        total_w = np.sum(weights)
        if total_w > 0:
            weights /= total_w
        else:
            weights = np.ones(num_particles) / num_particles  # Safeguard for zero likelihood

        # update empirical distributions
        for s in range(num_states):
            empirical_dists[t, s] = np.sum(weights[particles[:, t] == s])
            
    return particles, empirical_dists


def particle_filter_continuous(
    alpha_param: float,
    observations: np.ndarray,
    num_particles: int,
    sigma_x: float = 1.0,
    sigma_y: float = 3.0,
    use_resampling: bool = True
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Continuous Sequential Importance Sampling / Particle Filter for Gaussian HMM.
    
    :return: Tuple of (particles, estimated_means, estimated_stds)
    """
    sim_length = len(observations)
    particles = np.zeros((num_particles, sim_length))
    
    # Tablice na statystyki rozkładu filtrującego w czasie t
    est_means = np.zeros(sim_length)
    est_stds = np.zeros(sim_length)
    
    # Inicjalizacja wag i cząsteczek dla t = 0
    weights = np.ones(num_particles) / num_particles
    particles[:, 0] = np.random.normal(0, sigma_x, size=num_particles)
    
    # Ewaluacja wag za pomocą gęstości Gaussa: N(observations[0]; mean=particles, std=sigma_y)
    # Wzór na gęstość: (1 / sqrt(2*pi*sigma^2)) * exp(-(y - x)^2 / (2*sigma^2))
    likelihood = (1.0 / (sigma_y * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((observations[0] - particles[:, 0]) / sigma_y)**2)
    weights *= likelihood
    weights /= np.sum(weights)
    
    # Zapisz średnią ważoną i odchylenie standardowe populacji jako nasz ciągły rozkład
    est_means[0] = np.sum(particles[:, 0] * weights)
    est_stds[0] = np.sqrt(np.sum(weights * (particles[:, 0] - est_means[0])**2))
    
    for t in range(1, sim_length):
        if use_resampling:
            # Resampling wielomianowy cząsteczek
            cdf = np.cumsum(weights)
            r = np.random.rand(num_particles, 1)
            resample_idx = np.sum(r > cdf, axis=1)
            
            particles = particles[resample_idx, :]
            weights = np.ones(num_particles) / num_particles
            
        # Krok przejścia (Propagacja do przodu): X_t ~ N(alpha * X_{t-1}, sigma_x^2)
        mean_transitions = alpha_param * particles[:, t-1]
        particles[:, t] = np.random.normal(mean_transitions, sigma_x)
        
        # Aktualizacja wag (Likelihood nowej obserwacji)
        likelihood = (1.0 / (sigma_y * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((observations[t] - particles[:, t]) / sigma_y)**2)
        weights *= likelihood
        
        total_w = np.sum(weights)
        if total_w > 0:
            weights /= total_w
        else:
            weights = np.ones(num_particles) / num_particles
            
        # Wyliczenie parametrów ciągłego rozkładu empirycznego w kroku t
        est_means[t] = np.sum(particles[:, t] * weights)
        est_stds[t] = np.sqrt(np.sum(weights * (particles[:, t] - est_means[t])**2))
        
    return particles, est_means, est_stds



##############################
# Analysis
##############################


def analysis_total_variation_distance(exact_dist: np.ndarray, empirical_dist: np.ndarray) -> np.ndarray:
    """
    Calculate the Total Variation Distance (TVD) for each time step.

    :param exact_dist: Exact filtering distribution from FFBS (Ground Truth), shape (sim_length, num_states).
    :type exact_dist: np.ndarray
    :param empirical_dist: Approximated filtering distribution from SIS/PF, shape (sim_length, num_states).
    :type empirical_dist: np.ndarray
    :return: 1D array representing the TVD error value per time step.
    :rtype: np.ndarray
    """
    return 0.5 * np.sum(np.abs(exact_dist - empirical_dist), axis=1)


def analysis_kullback_leibler_divergence(exact_dist: np.ndarray, empirical_dist: np.ndarray) -> np.ndarray:
    """
    Calculate Kullback-Leibler Divergence KL(Exact || Empirical) for each time step with epsilon regularization.

    :param exact_dist: Exact filtering distribution from FFBS (Ground Truth), shape (sim_length, num_states).
    :type exact_dist: np.ndarray
    :param empirical_dist: Approximated filtering distribution from SIS/PF, shape (sim_length, num_states).
    :type empirical_dist: np.ndarray
    :return: 1D array representing the KL divergence value per time step.
    :rtype: np.ndarray
    """
    eps = 1e-12
    p = np.clip(exact_dist, eps, 1.0)
    p /= np.sum(p, axis=1, keepdims=True)
    
    q = np.clip(empirical_dist, eps, 1.0)
    q /= np.sum(q, axis=1, keepdims=True)
    
    return np.sum(p * np.log(p / q), axis=1)


def analysis_plot_state_distributions_with_errors(
    time_slices: list[int], 
    exact_dist: np.ndarray, 
    sis_dist: np.ndarray, 
    pf_dist: np.ndarray
) -> None:
    """
    Plot stacked bar charts of state distributions for Exact, SIS, and PF models.
    Displays computed TVD and KLD values directly above the corresponding SIS and PF bars with clean formatting.

    :param time_slices: List of specific indices along the time axis to visualize.
    :type time_slices: list[int]
    :param exact_dist: Ground truth filtering distribution, shape (sim_length, num_states).
    :type exact_dist: np.ndarray
    :param sis_dist: Empirical distribution from SIS, shape (sim_length, num_states).
    :type sis_dist: np.ndarray
    :param pf_dist: Empirical distribution from PF, shape (sim_length, num_states).
    :type pf_dist: np.ndarray
    """
    num_states = exact_dist.shape[1]
    
    # Calculate performance metrics over time
    sis_tvd = analysis_total_variation_distance(exact_dist, sis_dist)
    pf_tvd = analysis_total_variation_distance(exact_dist, pf_dist)
    sis_kl = analysis_kullback_leibler_divergence(exact_dist, sis_dist)
    pf_kl = analysis_kullback_leibler_divergence(exact_dist, pf_dist)
    
    # Define custom styling patterns as explicitly requested
    state_colors = plt.cm.get_cmap('tab10')(np.linspace(0, 1, num_states))
    method_hatches = ['..', '-', '//']  # GT = kropki (dots), SIS = proste (vertical), PF = pod kątem (diagonal)
    
    fig, ax = plt.subplots(figsize=(15, 9))
    
    bar_width = 0.25
    group_spacing = 1.3
    
    for idx, t in enumerate(time_slices):
        base_x = idx * group_spacing
        
        pos_exact = base_x - bar_width
        pos_sis = base_x
        pos_pf = base_x + bar_width
        
        # 1. Plot Exact Stacked Bar (Ground Truth) -> Kropki '..'
        bottom_exact = 0.0
        for s in range(num_states):
            val = exact_dist[t, s]
            ax.bar(pos_exact, val, bar_width, bottom=bottom_exact, color=state_colors[s], 
                   edgecolor='black', hatch=method_hatches[0], label=f'State {s}' if idx == 0 else "")
            bottom_exact += val
        ax.text(pos_exact, 1.02, 'GT', ha='center', va='bottom', fontsize=8, fontweight='bold')
            
        # 2. Plot SIS Stacked Bar ->  '-'
        bottom_sis = 0.0
        for s in range(num_states):
            val = sis_dist[t, s]
            ax.bar(pos_sis, val, bar_width, bottom=bottom_sis, color=state_colors[s], 
                   edgecolor='black', hatch=method_hatches[1])
            bottom_sis += val
        # Format text to separate metrics onto distinct lines to avoid overlapping
        sis_text = f"TVD:\n{sis_tvd[t]:.3f}\nKL:\n{sis_kl[t]:.3f}"
        ax.text(pos_sis, 1.02, sis_text, ha='center', va='bottom', fontsize=8, color='crimson')
            
        # 3. Plot PF Stacked Bar ->  '//'
        bottom_pf = 0.0
        for s in range(num_states):
            val = pf_dist[t, s]
            ax.bar(pos_pf, val, bar_width, bottom=bottom_pf, color=state_colors[s], 
                   edgecolor='black', hatch=method_hatches[2])
            bottom_pf += val
        # Format text to separate metrics onto distinct lines to avoid overlapping
        pf_text = f"TVD:\n{pf_tvd[t]:.3f}\nKL:\n{pf_kl[t]:.3f}"
        ax.text(pos_pf, 1.02, pf_text, ha='center', va='bottom', fontsize=8, color='teal')

    # Formatting axes and labels
    ax.set_ylabel('Probability Distribution (Sums to 1.0)')
    ax.set_title('Filtering State Probability Distribution Comparison with Split Margin Errors')
    ax.set_xticks([i * group_spacing for i in range(len(time_slices))])
    ax.set_xticklabels([f't = {t}' for t in time_slices])
    ax.set_ylim(0, 1.35)  # Extended height to accommodate multi-line overhead text strings Safely
    
    # Custom legends for pattern types
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='white', edgecolor='black', hatch=method_hatches[0], label='Exact (GT - Dots)'),
        Patch(facecolor='white', edgecolor='black', hatch=method_hatches[1], label='SIS (Straight Lines)'),
        Patch(facecolor='white', edgecolor='black', hatch=method_hatches[2], label='PF (Angled Lines)')
    ]
    for s in range(num_states):
        legend_elements.append(Patch(facecolor=state_colors[s], edgecolor='black', label=f'State {s}'))
        
    ax.legend(handles=legend_elements, loc='upper right')
    plt.tight_layout()
    plt.show()


def analysis_plot_convergence_rate(
    initial_dist: np.ndarray,
    transition_matrix: np.ndarray,
    emission_matrix: np.ndarray,
    observations: np.ndarray,
    particle_counts: list[int]
) -> None:
    """
    Analyze and plot the convergence rate of SIS and PF models as the particle count increases.
    Computes mean metric distances (TVD and KLD) across the entire trajectory duration against Ground Truth.

    :param initial_dist: Initial state distribution vector, shape (num_states,).
    :type initial_dist: np.ndarray
    :param transition_matrix: Transition matrix T, shape (num_states, num_states).
    :type transition_matrix: np.ndarray
    :param emission_matrix: Emission matrix L, shape (num_states, num_obs_types).
    :type emission_matrix: np.ndarray
    :param observations: Sequence array of observed indexes, shape (sim_length,).
    :type observations: np.ndarray
    :param particle_counts: List containing different particle capacities (N) to evaluate.
    :type particle_counts: list[int]
    """
    # Obtain precise analytical filtering distribution
    exact_dist = forward_filtering_backward_sampling(
        initial_dist, transition_matrix, emission_matrix, observations, num_samples=0
    )
    
    sis_mean_tvds, pf_mean_tvds = [], []
    sis_mean_klds, pf_mean_klds = [], []
    
    for n in particle_counts:
        initial_weights = np.ones(n) / n
        
        # Run simulations using the current particle setup
        _, sis_dist = particle_filter_sis_pfs(
            initial_dist, initial_weights, transition_matrix, emission_matrix, observations, 
            num_particles=n, use_resampling=False
        )
        _, pf_dist = particle_filter_sis_pfs(
            initial_dist, initial_weights, transition_matrix, emission_matrix, observations, 
            num_particles=n, use_resampling=True
        )
        
        # Calculate full sequence errors
        sis_tvd = analysis_total_variation_distance(exact_dist, sis_dist)
        pf_tvd = analysis_total_variation_distance(exact_dist, pf_dist)
        sis_kl = analysis_kullback_leibler_divergence(exact_dist, sis_dist)
        pf_kl = analysis_kullback_leibler_divergence(exact_dist, pf_dist)
        
        # Extract mean values across the entire observation trajectory
        sis_mean_tvds.append(np.mean(sis_tvd))
        pf_mean_tvds.append(np.mean(pf_tvd))
        sis_mean_klds.append(np.mean(sis_kl))
        pf_mean_klds.append(np.mean(pf_kl))
        
    # Generate line visualization plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # TVD Convergence Plot
    ax1.plot(particle_counts, sis_mean_tvds, marker='o', linestyle='--', color='crimson', label='SIS (No Resampling)')
    ax1.plot(particle_counts, pf_mean_tvds, marker='s', linestyle='-', color='teal', label='PF (With Resampling)')
    ax1.set_xlabel('Number of Particles (N)')
    ax1.set_ylabel('Mean Total Variation Distance (TVD)')
    ax1.set_title('Convergence Speed: Mean TVD Error vs Particle Count')
    ax1.grid(True, linestyle=':')
    ax1.legend()
    
    # KLD Convergence Plot
    ax2.plot(particle_counts, sis_mean_klds, marker='o', linestyle='--', color='crimson', label='SIS (No Resampling)')
    ax2.plot(particle_counts, pf_mean_klds, marker='s', linestyle='-', color='teal', label='PF (With Resampling)')
    ax2.set_xlabel('Number of Particles (N)')
    ax2.set_ylabel('Mean Kullback-Leibler Divergence (KLD)')
    ax2.set_title('Convergence Speed: Mean KLD Error vs Particle Count')
    ax2.grid(True, linestyle=':')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()