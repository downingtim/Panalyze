import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
import base64

# Helper function to display PDFs
def display_pdf(file_path, height=600):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{height}" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.info(f"File not found: {file_path}")

# Helper function to display text/dataframes
def display_text_file(file_path, is_tsv=False):
    if os.path.exists(file_path):
        if is_tsv:
            df = pd.read_csv(file_path, sep="\t", header=None)
            st.dataframe(df, use_container_width=True)
        else:
            with open(file_path, "r") as f:
                st.text(f.read())
    else:
        st.info(f"File not found: {file_path}")

st.set_page_config(page_title="Panalyze Dashboard", layout="wide")

st.title("🦠 Panalyze Interactive Dashboard")
st.markdown("Comprehensive interactive exploration of Pangenome Variation Graph (PVG) results.")

# --- SIDEBAR ---
st.sidebar.header("Data Options")
results_dir = st.sidebar.text_input("Path to Panalyze 'results' folder:", value="../results")

if not os.path.exists(results_dir):
    st.sidebar.error(f"Directory not found: {results_dir}")
    st.stop()

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Pangenome Growth", 
    "Graph Structure", 
    "Variants & Mutations", 
    "Phylogeny & Communities",
    "Annotations & Metadata",
    "Raw Data Preview"
])

# --- TAB 1: Pangenome Growth ---
with tab1:
    st.header("Pangenome Growth (Heaps' Law & Openness)")
    
    col1, col2 = st.columns(2)
    with col1:
        heaps_path = os.path.join(results_dir, "heaps", "heaps.txt")
        if os.path.exists(heaps_path):
            heaps_df = pd.read_csv(heaps_path, sep="\t", header=None, names=["Max", "Samples", "Size"])
            heaps_df = heaps_df.iloc[::-1].reset_index(drop=True)
            heaps_df['Fraction'] = range(1, len(heaps_df) + 1)
            
            fig_heaps = px.line(heaps_df, x="Fraction", y="Size", markers=True, title="Heaps' Law: Pangenome Growth")
            fig_heaps.update_traces(line_color='#e74c3c')
            st.plotly_chart(fig_heaps, use_container_width=True)
        else:
            st.info("heaps.txt not found.")
            
    with col2:
        st.subheader("Panacus Openness")
        display_pdf(os.path.join(results_dir, "panacus", "histgrowth.node.pdf"), height=400)

    st.divider()
    st.subheader("Pangrowth & Core Genome")
    display_pdf(os.path.join(results_dir, "pangrowth", "pangrowth.pdf"), height=500)

# --- TAB 2: Graph Structure ---
with tab2:
    st.header("Graph Structure & Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("GFA Statistics")
        display_text_file(os.path.join(results_dir, "gfastat", "gfa.stats.txt"))
    with col2:
        st.subheader("ODGI Statistics")
        display_text_file(os.path.join(results_dir, "odgi", "odgi.stats.txt"))

    st.divider()
    st.subheader("VG Visualization (Graph)")
    vg_path = os.path.join(results_dir, "vg", "out.vg.png")
    if os.path.exists(vg_path):
        with open(vg_path, "rb") as file:
            st.download_button("📥 Download full VG Image", data=file, file_name="out.vg.png", mime="image/png")

    st.subheader("ODGI Visualization (Viz2)")
    viz2_path = os.path.join(results_dir, "viz2", "out.viz.png")
    if os.path.exists(viz2_path):
        with open(viz2_path, "rb") as file:
            st.download_button("📥 Download full Viz2 Image", data=file, file_name="out.viz.png", mime="image/png")

# --- TAB 3: Variants & Mutations ---
with tab3:
    st.header("Variants & Mutations")
    
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
        
        fig_mut = px.histogram(df_variants, x="Position", nbins=100, title="Mutation Density across Genome")
        st.plotly_chart(fig_mut, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Presence/Absence Variants (PAVs)")
        display_pdf(os.path.join(results_dir, "pavs", "out.flatten.pavs.pdf"), height=450)
    with col2:
        st.subheader("Allele Frequency Spectrum")
        afs_png = os.path.join(results_dir, "vcf", "frequency_distribution.png")
        afs_txt = os.path.join(results_dir, "vcf", "afs_counts.txt")
        if os.path.exists(afs_png):
            st.image(afs_png, use_container_width=True)
        else:
            display_text_file(afs_txt)

# --- TAB 4: Phylogeny & Communities ---
with tab4:
    st.header("Phylogeny & Communities")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("RAxML Phylogeny")
        tree_path = os.path.join(results_dir, "tree", "tree.png")
        if os.path.exists(tree_path):
            st.image(tree_path, use_container_width=True)
        else:
            st.info("Tree image not found.")
    with col2:
        st.subheader("Communities Network")
        display_pdf(os.path.join(results_dir, "communities", "communities.pdf"), height=450)

# --- TAB 5: Annotations & Metadata ---
with tab5:
    st.header("Annotations & Metadata")
    
    st.subheader("Node to Feature Mapping (Annotation)")
    annot_path = os.path.join(results_dir, "annotation", "node_to_feature.tsv")
    if not os.path.exists(annot_path):
        annot_path = os.path.join(results_dir, "bandage", "PVG_annotation.csv")
        
    if annot_path.endswith(".csv"):
        if os.path.exists(annot_path):
            df = pd.read_csv(annot_path)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Annotation file not found.")
    else:
        display_text_file(annot_path, is_tsv=True)

    st.divider()
    st.subheader("Sample Metadata")
    meta_path = os.path.join(results_dir, "download", "metadata.tsv")
    display_text_file(meta_path, is_tsv=True)

# --- TAB 6: Raw Data Preview ---
with tab6:
    st.header("Raw Data Preview")
    st.markdown("Preview text files directly without downloading.")
    
    raw_files = {
        "Heaps Raw": os.path.join(results_dir, "heaps", "heaps.txt"),
        "Sample Paths": os.path.join(results_dir, "pvg", "sample_paths.txt"),
        "Genome Lengths": os.path.join(results_dir, "gfastat", "genome.lengths.txt"),
    }
    
    file_choice = st.selectbox("Select a file to preview:", list(raw_files.keys()))
    if file_choice:
        display_text_file(raw_files[file_choice])