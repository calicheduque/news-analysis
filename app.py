
with st.sidebar:
    st.markdown("## Run configuration")
    mode_label = st.radio(
        "Execution mode",
        ["Demo preview", "Live backend"],
        index=0,
        help="Demo preview runs locally without credentials. Live backend sends the claim to your team's API.",
    )
    api_url = DEFAULT_API_URL
    if mode_label == "Live backend":
        api_url = st.text_input("Research API URL", value=DEFAULT_API_URL)
        st.caption(f"Request timeout: {REQUEST_TIMEOUT}s")
    else:
        st.success("Ready to preview locally")
        st.caption("No external API is called in demo mode.")
    st.markdown("---")
    st.markdown("### Evidence labels")
    for label, description in [
        ("PUBLIC", "Published sources and official data"),
        ("HUMAN", "Responses from real participants"),
        ("SYNTHETIC", "AI-generated or simulated responses"),
        ("UNVERIFIED", "Not yet supported by adequate evidence"),
    ]:
        st.markdown(f"{tag(label)} {description}", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Never present synthetic responses as human testimony. Never invent sample sizes, quotes, or source citations.")

st.markdown('<div class="section-kicker">Start an investigation</div>', unsafe_allow_html=True)
with st.form("investigation_form"):
    claim = st.text_area(
        "Public claim to investigate",
        value=DEFAULT_CLAIM,
        height=96,
        placeholder="Example: Rent prices are falling in NYC.",
        help="Use a specific, falsifiable claim. The backend should clarify geography, time period, population, and metric.",
    )
    submitted = st.form_submit_button("↗  Investigate", type="primary", use_container_width=True)

if submitted:
    if not claim.strip():
        st.error("Enter a claim before starting the investigation.")
    else:
        with st.status("Preparing investigation…", expanded=True) as status_box:
            if mode_label == "Demo preview":
                st.write("✓ Claim received")
                st.write("✓ Demo response prepared")
                st.write("! Public retrieval and Flashpoint survey were not run")
                result = make_demo_result(claim.strip())
                status_box.update(label="Demo preview ready", state="complete", expanded=False)
            else:
                st.write("Submitting claim to your research backend…")
                try:
                    result = call_backend(claim.strip(), api_url)
                    status_box.update(label="Backend response received", state="complete", expanded=False)
                except requests.Timeout:
                    result = None
                    status_box.update(label="Research backend timed out", state="error", expanded=True)
                    st.error("The backend did not respond before the timeout. Check its logs and try again.")
                except requests.ConnectionError:
                    result = None
                    status_box.update(label="Cannot connect to research backend", state="error", expanded=True)
                    st.error("Could not reach the backend. Confirm that its local server is running and the URL is correct.")
                except requests.HTTPError as exc:
                    result = None
                    status_box.update(label="Research backend returned an HTTP error", state="error", expanded=True)
                    st.error(f"Backend HTTP error: {exc}")
                    if exc.response is not None:
                        st.code(exc.response.text[:3000])
                except (ValueError, requests.RequestException) as exc:
                    result = None
                    status_box.update(label="Could not process backend response", state="error", expanded=True)
                    st.error(str(exc))
                except Exception as exc:  # Keep UI errors visible during the hackathon demo.
                    result = None
                    status_box.update(label="Unexpected error", state="error", expanded=True)
                    st.exception(exc)

        if result:
            st.session_state["last_result"] = result
            st.session_state["last_mode"] = result.get("mode", "live")

if "last_result" in st.session_state:
    last_result = st.session_state["last_result"]
    render_stage_status(last_result.get("stages", {}), st.session_state.get("last_mode", "live"))
    render_article(last_result)
else:
    st.markdown("---")
    st.markdown("### One flow. One article.")
    st.markdown(
        "The live version connects three operations: public-source research, participant research through Flashpoint, "
        "and evidence synthesis. The UI keeps the origin of every finding visible."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Input", "1 public claim")
    c2.metric("Research", "Public + people")
    c3.metric("Output", "1 evidence-led article")

st.markdown(
    '<div class="footer-note">The Gap is a research prototype, not a fact-checking authority. Claims require source verification, survey methodology, and human review before publication.</div>',
    unsafe_allow_html=True,
)
