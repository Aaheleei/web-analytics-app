import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import pandas as pd
import plotly.express as px
import streamlit as st

# Import modular services
from app.database.db import fetch_all_launches, save_launch_metrics
from app.services.nlp import analyze_headlines_sentiment
from app.services.scraper import fetch_google_news, fetch_wikipedia_pageviews

# Page Config
st.set_page_config(
    page_title="Web & Social Media Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 Web & Social Media Analytics Dashboard")
st.caption(
    "Lab Curriculum Implementation: Scraping, Preprocessing & NLP, Sentiment Analysis, and Visualization & Reporting."
)

# Sidebar Form Input
with st.sidebar:
    st.header("Analytics Target")
    with st.form(key="search_form"):
        show_title_input = st.text_input(
            "Enter Show/Movie Title:", value="Wednesday"
        )
        submit_btn = st.form_submit_button("Run Analytics 🚀")

if submit_btn and show_title_input.strip():
    show_title = show_title_input.strip()

    # Data Collection via Scraper
    raw_articles = fetch_google_news(show_title)

    if not raw_articles:
        st.warning(
            f"No recent news articles found for '{show_title}'. Try another title."
        )
    else:
        # NLP Preprocessing & Sentiment Analysis
        processed_articles, summary = analyze_headlines_sentiment(
            raw_articles, show_title
        )
        df_articles = pd.DataFrame(processed_articles)
        unique_publishers = df_articles["publisher"].nunique()

        # Database Logging
        save_launch_metrics(
            show_title=show_title,
            article_volume=summary["total_items"],
            publisher_count=unique_publishers,
            net_sentiment=summary["avg_compound"],
            positive_hype_pct=summary["pos_pct"],
        )

        # Render 4 Tabs matching the Lab Manual Curriculum
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🌐 1. Web Scraping & Data Collection",
                "🔤 2. Text Preprocessing & NLP",
                "🎭 3. Sentiment Analysis",
                "📊 4. Visualization & Reporting",
            ]
        )

        # TAB 1: Web Scraping and Data Collection
        with tab1:
            st.subheader(
                f"1. Web Scraping & Media Data Collection for '{show_title}'"
            )

            col1, col2 = st.columns(2)
            col1.metric("Total Articles Scraped", summary["total_items"])
            col2.metric("Unique Publishers Extracted", unique_publishers)

            st.markdown("---")
            st.write("### Raw Scraped Headlines & Publishers Payload")
            st.dataframe(
                df_articles[["headline", "publisher", "published", "link"]],
                use_container_width=True,
            )

        # TAB 2: Text Preprocessing & NLP
        with tab2:
            st.subheader("2. Text Preprocessing & NLP Pipeline")
            st.info(
                "Title-Agnostic Cleaning applied: The exact target title string is stripped before NLTK VADER evaluation to eliminate lexical bias."
            )

            col1, col2 = st.columns(2)
            col1.metric(
                "Mean Polarity Score",
                summary["avg_compound"],
                help="VADER compound polarity from -1.0 to +1.0",
            )
            col2.metric(
                "Neutral Text Ratio", f"{summary['neu_pct']}%"
            )

            st.markdown("---")
            st.write("### Cleaned NLP Payload & VADER Score Breakdown")
            st.dataframe(
                df_articles[
                    ["headline", "pos", "neu", "neg", "compound", "sentiment"]
                ],
                use_container_width=True,
            )

        # TAB 3: Sentiment Analysis
        with tab3:
            st.subheader("3. Sentiment Analysis & Distribution")

            col1, col2, col3 = st.columns(3)
            col1.metric("Net Sentiment Compound", summary["avg_compound"])
            col2.metric("Positive Sentiment Ratio", f"{summary['pos_pct']}%")
            col3.metric("Negative Sentiment Ratio", f"{summary['neg_pct']}%")

            st.markdown("---")
            col_chart, col_summary = st.columns([1, 1])

            with col_chart:
                st.write("### Sentiment Ratio Breakdown")
                sentiment_counts = (
                    df_articles["sentiment"].value_counts().reset_index()
                )
                sentiment_counts.columns = ["Sentiment", "Count"]

                fig_donut = px.pie(
                    sentiment_counts,
                    names="Sentiment",
                    values="Count",
                    color="Sentiment",
                    color_discrete_map={
                        "Positive": "#2ECC71",
                        "Neutral": "#95A5A6",
                        "Negative": "#E74C3C",
                    },
                    hole=0.4,
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            with col_summary:
                st.write("### Sentiment Export & Summary")
                st.dataframe(
                    df_articles[["headline", "sentiment", "compound"]],
                    use_container_width=True,
                )

                csv_data = df_articles.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Export Sentiment Report (CSV)",
                    data=csv_data,
                    file_name=f"{show_title}_sentiment_analysis.csv",
                    mime="text/csv",
                )

        # TAB 4: Visualization & Reporting (plus Web Analytics)
        with tab4:
            st.subheader("4. Visualization, Reporting & Web Analytics")

            # 30-Day Wikipedia Traffic Trends
            st.write("### Web Analytics: 30-Day Wikipedia Audience Traffic")
            wiki_views = fetch_wikipedia_pageviews(show_title)

            if wiki_views:
                df_wiki = pd.DataFrame(wiki_views)
                fig_line = px.line(
                    df_wiki,
                    x="date",
                    y="views",
                    title=f"Daily Wikipedia Readers for '{show_title}'",
                    markers=True,
                )
                fig_line.update_layout(
                    xaxis_title="Date", yaxis_title="Pageviews"
                )
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("No Wikipedia pageview data found.")

            st.markdown("---")

            # Cross-Campaign Database Reporting
            st.write("### Historical Reporting & Campaign Benchmarks (SQLite)")
            history_rows = fetch_all_launches()
            if history_rows:
                df_history = pd.DataFrame(
                    history_rows,
                    columns=[
                        "Show Title",
                        "Article Volume",
                        "Publisher Count",
                        "Net Sentiment",
                        "Positive Hype %",
                        "Timestamp",
                    ],
                )
                st.dataframe(df_history, use_container_width=True)

                fig_bar = px.bar(
                    df_history,
                    x="Show Title",
                    y="Net Sentiment",
                    color="Show Title",
                    title="Cross-Campaign Net Sentiment Comparison",
                )
                fig_bar.update_layout(
                    yaxis_range=[-1, 1], yaxis_title="Net Sentiment Score"
                )
                st.plotly_chart(fig_bar, use_container_width=True)