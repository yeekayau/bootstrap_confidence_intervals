# Save this code in a file named `bootstrap_dotplot_app.py`

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

def bootstrap_dotplot(sample_size=200, proportion=0.275, num_bootstrap_samples=1000, bins=40):
    # Generate bootstrap sample proportions
    bootstrap_samples = binom.rvs(n=sample_size, p=proportion, size=num_bootstrap_samples) / sample_size
    
    # Calculate the mean and standard deviation of the bootstrap sample proportions
    mean_proportion = np.mean(bootstrap_samples)
    std_error = np.std(bootstrap_samples)
    
    # Bin the data to calculate dot positions for each sample proportion
    counts, bin_edges = np.histogram(bootstrap_samples, bins=bins)
    x = []
    y = []
    colors = []
    red_dot_count = 0  # Counter for red dots
    
    # Classify points based on their distance from the mean
    for i, count in enumerate(counts):
        # Calculate the midpoint of each bin
        bin_midpoint = (bin_edges[i] + bin_edges[i+1]) / 2
        color = 'red' if abs(bin_midpoint - mean_proportion) >= 2 * std_error else 'royalblue'
        
        x.extend([bin_midpoint] * count)  # Repeat each bin's x position
        y.extend(range(count))            # y positions are stacked up for each bin
        colors.extend([color] * count)    # Assign color based on distance from the mean
        
        # Count red dots
        if color == 'red':
            red_dot_count += count

    # Calculate the proportion of red dots
    total_dots = len(x)
    red_dot_proportion = red_dot_count / total_dots if total_dots > 0 else 0

    # Create the plotly dot plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers',
        marker=dict(size=4, color=colors, line=dict(width=0.0, color='black')),
        opacity=0.7,
        showlegend=False
    ))

    # Customize layout to make it narrower and display estimated standard error
    fig.update_layout(
        title=f'Bootstrap Distribution of Sample Proportions (n={sample_size}, p={proportion})',
        xaxis_title='Sample Proportion',
        yaxis_title='Frequency',
        width=1600,  # Double the width
        height=600,  # Double the height
        xaxis=dict(tickformat=".2f", dtick=0.01),
        plot_bgcolor='#f9f9f9',
        yaxis=dict(showgrid=False, zeroline=False),
        annotations=[
            dict(
                x=0.5, y=1.1, xref="paper", yref="paper",
                text=f"Estimated Standard Error: {std_error:.4f}",
                showarrow=False,
                font=dict(size=12)
            )
        ]
    )

    return fig, std_error, red_dot_proportion

# Streamlit app layout
st.title("Bootstrap Distribution of Sample Proportions")

# Input fields
sample_size = st.number_input("Sample Size", min_value=10, max_value=20000, value=200, step=10)
proportion = st.number_input("Proportion", min_value=0.0, max_value=1.0, value=0.275, step=0.01)
num_bootstrap_samples = st.number_input("Number of Bootstrap Samples", min_value=100, max_value=20000, value=1000, step=100)

# Generate plot
fig, std_error, red_dot_proportion = bootstrap_dotplot(sample_size, proportion, num_bootstrap_samples)
st.plotly_chart(fig)

# Display the estimated standard error and proportion of red dots
st.write(f"**Estimated Standard Error:** {std_error:.4f}")
st.write(f"**Proportion of Red Dots (2 or more SDs from Mean):** {red_dot_proportion:.4%}")
