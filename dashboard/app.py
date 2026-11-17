import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
import base64

# Helper function to display PDFs in Streamlit
def display_pdf(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.info(f"File not found: {file_path}")

st.set_page_config(page_title="Panalyze Dashboard", layout="wide")

st.title("🦠 Panalyze Variation Graph Dashboard")
st.markdown("Interactive exploration of Pangenome Variation Graph (PVG) metrics.")

# --- SIDEBAR ---
st.sidebar.header("Data Options")
# Default to '../results' assuming the dashboard is inside the Panalyze repo
results_dir = st.sidebar.text_input("Path to Panalyze 'results' folder:", value="../results")

if not os.path.exists(results_dir):
    st.sidebar.error(f"Directory not found: {results_dir}")
    st.stop()

# Load haplotypes if it exists
haplotypes_path = os.path.join(results_dir, "panacus", "haplotypes.txt")
if not os.path.exists(haplotypes_path):
    haplotypes_path = os.path.join(results_dir, "haplotypes.txt")
    
if os.path.exists(haplotypes_path):
    haplotypes = pd.read_csv(haplotypes_path, header=None, names=["Genome"])
    st.sidebar.write(f"**Genomes loaded:** {len(haplotypes)}")
    st.sidebar.dataframe(haplotypes, use_container_width=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Pangenome Growth", 
    "Graph Complexity", 
    "Mutations & PAVs", 
    "Openness Metrics",
    "Phylogeny & Visuals"
])

# --- TAB 1: Pangenome Growth ---
with tab1:
    st.header("Pangenome Growth (Heaps' Law)")
    heaps_path = os.path.join(results_dir, "heaps", "heaps.txt")
    
    if os.path.exists(heaps_path):
        heaps_df = pd.read_csv(heaps_path, sep="\t", header=None, names=["Max_Samples", "Sample_Count", "Pangenome_Size"])
        
        # --- FIX: Reverse the dataframe so it goes from smallest to largest ---
        heaps_df = heaps_df.iloc[::-1].reset_index(drop=True)
        heaps_df['Fraction of Samples'] = range(1, len(heaps_df) + 1)
        
        fig_heaps = px.line(heaps_df, x="Fraction of Samples", y="Pangenome_Size", 
                            markers=True, title="Sample fraction vs Pangenome Size")
        fig_heaps.update_traces(line_color='#e74c3c', marker=dict(size=8, color='#c0392b'))
        fig_heaps.update_layout(xaxis_title="Fraction of Samples", yaxis_title="Number of Bases in Paths")
        
        st.plotly_chart(fig_heaps, use_container_width=True)

# --- TAB 2: Graph Complexity ---
with tab2:
    st.header("Graph Complexity & Node Growth")
    hist_path = os.path.join(results_dir, "panacus", "histgrowth.node.tsv")
    
    if os.path.exists(hist_path):
        with open(hist_path, "r") as f:
            lines = [line for line in f.readlines() if not line.startswith("#")]
        
        hist_df = pd.read_csv(io.StringIO("".join(lines)), sep="\t", skiprows=4, header=None)
        hist_df.columns = ["Samples", "Histogram_Count", "Cov1_Q0", "Cov2_Q0", "Cov1_Q100", "Cov1_Q50", "Cov1_Q10"]
        
        growth_df = hist_df.drop(columns=["Histogram_Count"])
        hist_melted = growth_df.melt(id_vars=["Samples"], var_name="Coverage/Quorum Filter", value_name="Number of Nodes")
        
        label_map = {
            "Cov1_Q0": "cov ≥ 1, q ≥ 0%", "Cov2_Q0": "cov ≥ 2, q ≥ 0%",
            "Cov1_Q100": "cov ≥ 1, q ≥ 100%", "Cov1_Q50": "cov ≥ 1, q ≥ 50%",
            "Cov1_Q10": "cov ≥ 1, q ≥ 10%"
        }
        hist_melted["Coverage/Quorum Filter"] = hist_melted["Coverage/Quorum Filter"].map(label_map)
        
        fig_nodes = px.bar(hist_melted, x="Samples", y="Number of Nodes", color="Coverage/Quorum Filter",
                           barmode="group", title="Growth of Nodes based on Coverage & Quorum")
        st.plotly_chart(fig_nodes, use_container_width=True)
    else:
        st.info(f"histgrowth.node.tsv not found at {hist_path}")
        
    st.divider()
    st.subheader("Panacus PDF Output")
    display_pdf(os.path.join(results_dir, "panacus", "histgrowth.node.pdf"))

# --- TAB 3: Mutations & PAVs ---
with tab3:
    st.header("Mutation Density")
    vcf_path = os.path.join(results_dir, "vcf", "gfavariants.vcf")
    
    if os.path.exists(vcf_path):
        vcf_data = []
        with open(vcf_path, 'r') as f:
            for line in f:
                if not line.startswith('#'):
                    parts = line.strip().split('\t')
                    if len(parts) > 1:
                        vcf_data.append(int(parts[1]))
                        
        df_variants = pd.DataFrame(vcf_data, columns=["Position"])
        fig_mut = px.histogram(df_variants, x="Position", nbins=100, 
                               title="Mutation Density across the Genome",
                               labels={'Position': 'Genomic Position (bp)', 'y': 'Frequency'})
        fig_mut.update_layout(bargap=0.1, yaxis_title="Frequency (Count)")
        st.plotly_chart(fig_mut, use_container_width=True)
    else:
        st.warning(f"VCF not found at {vcf_path}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Allele Frequency Distribution")
        freq_png_path = os.path.join(results_dir, "vcf", "frequency_distribution.png")
        if os.path.exists(freq_png_path):
            st.image(freq_png_path, use_container_width=True)
        else:
            st.info("Frequency plot not found.")
            
    with col2:
        st.subheader("Presence/Absence Variants (PAVs)")
        st.markdown("Structural variations across genomes.")
        display_pdf(os.path.join(results_dir, "pavs", "out.flatten.pavs.pdf"))

# --- TAB 4: Openness Metrics ---
with tab4:
    st.header("Pangenome Openness")
    st.markdown("Metrics showing how 'open' (highly variable) or 'closed' (conserved) the pangenome is.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pangrowth")
        display_pdf(os.path.join(results_dir, "pangrowth", "pangrowth.pdf"))
    with col2:
        st.subheader("Core Genome Growth")
        display_pdf(os.path.join(results_dir, "pangrowth", "p_core.pdf"))

# --- TAB 5: Phylogeny & Visuals ---
with tab5:
    st.header("Phylogeny & Graph Visualizations")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Phylogenetic Tree")
        tree_path = os.path.join(results_dir, "tree", "tree.png")
        if os.path.exists(tree_path):
            st.image(tree_path, caption="RAxML Tree", use_container_width=True)
        else:
            st.info("Tree image not found.")
            
    with col2:
        st.subheader("Graph Structure (VG)")
        vg_path = os.path.join(results_dir, "vg", "out.vg.png")
        if os.path.exists(vg_path):
            st.info("ℹ️ The VG graph is extremely wide. Click below to download and view it in your image viewer.")
            with open(vg_path, "rb") as file:
                st.download_button(
                    label="📥 Download VG Graph Image",
                    data=file,
                    file_name="out.vg.png",
                    mime="image/png"
                )
        else:
            st.info(f"VG image not found at {vg_path}")
            
    st.divider()
    st.subheader("ODGI Visualization (Viz2)")
    viz2_path = os.path.join(results_dir, "viz2", "out.viz.png")
    if os.path.exists(viz2_path):
        st.info("ℹ️ The ODGI visualization is extremely wide. Click below to download and view it in your image viewer.")
        with open(viz2_path, "rb") as file:
            st.download_button(
                label="📥 Download ODGI Image",
                data=file,
                file_name="out.viz.png",
                mime="image/png"
            )
    else:
        st.info("Viz2 image not found.")