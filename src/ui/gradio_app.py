import gradio as gr
from services.optimization_service import CvOptimizationService


def create_app():
    """Create and configure the Gradio application."""

    service = CvOptimizationService()

    with gr.Blocks(title="CV Agents") as app:
        gr.Markdown("# CV Agents - Job-Optimized CV Generation")

        with gr.Tabs():
            # Tab 1: Job Postings
            with gr.Tab("Job Postings"):
                with gr.Group():
                    gr.Markdown("### Create New Job Posting")
                    job_url = gr.Textbox(
                        label="Job Posting URL",
                        placeholder="https://...",
                    )
                    analyze_job_btn = gr.Button("Analyze Job Posting", variant="primary")

                with gr.Group():
                    gr.Markdown("### Results")
                    job_result = gr.JSON(label="Job Posting Details")
                    job_identifier = gr.Textbox(
                        label="Save As",
                        placeholder="company-position",
                    )
                    job_is_saved = gr.State(value=False)
                    save_job_btn = gr.Button("Save Job Posting")
                    save_job_status = gr.Textbox(label="Status", interactive=False)

                with gr.Group():
                    gr.Markdown("### Saved Job Postings")
                    job_list_dropdown = gr.Dropdown(
                        label="Select Job Posting to View",
                        choices=[],
                        interactive=True,
                    )
                    view_job_btn = gr.Button("View Selected")
                    job_list = gr.Dataframe(
                        headers=["Identifier", "Company", "Position"],
                        label="All Job Postings",
                    )
                    refresh_jobs_btn = gr.Button("Refresh List")

                # Event handlers for Job Postings tab
                def analyze_job(url):
                    result = service.create_job_posting(url)
                    identifier = result.get("identifier", "")
                    is_saved = False
                    return result, identifier, is_saved, gr.update(interactive=True)

                def view_saved_job(identifier):
                    if not identifier:
                        return None, "", True, gr.update(interactive=False), ""

                    job_posting = service.repository.get_job_posting(identifier)
                    if not job_posting:
                        return None, "", True, gr.update(interactive=False), "⚠ Job posting not found"

                    result = job_posting.model_dump()
                    result["identifier"] = identifier
                    result["status"] = "loaded"
                    is_saved = True

                    return result, identifier, is_saved, gr.update(interactive=False), f"✓ Loaded: {identifier}"

                def save_job(job_data, identifier, is_saved):
                    if is_saved:
                        return "ℹ Job posting is already saved", None, True, gr.update(interactive=False)

                    if not job_data or not identifier:
                        return "⚠ Please analyze a job posting first and provide an identifier", None, False, gr.update(interactive=True)

                    try:
                        metadata = service.save_job_posting(job_data, identifier)
                        jobs = service.get_job_postings()
                        job_list_data = [
                            [j.get("identifier", ""), j.get("company", ""), j.get("title", "")]
                            for j in jobs
                        ]
                        job_choices = [(f"{j['company']} - {j['title']}", j['identifier']) for j in jobs]
                        return (
                            f"✓ Job posting saved: {metadata['identifier']}",
                            job_list_data,
                            True,
                            gr.update(interactive=False),
                        )
                    except Exception as e:
                        return f"✗ Error saving job posting: {str(e)}", None, False, gr.update(interactive=True)

                def load_jobs():
                    jobs = service.get_job_postings()
                    job_list_data = [
                        [j.get("identifier", ""), j.get("company", ""), j.get("title", "")]
                        for j in jobs
                    ]
                    job_choices = [(f"{j['company']} - {j['title']}", j['identifier']) for j in jobs]
                    return job_list_data, gr.update(choices=job_choices)

                analyze_job_btn.click(
                    fn=analyze_job,
                    inputs=[job_url],
                    outputs=[job_result, job_identifier, job_is_saved, save_job_btn],
                )

                view_job_btn.click(
                    fn=view_saved_job,
                    inputs=[job_list_dropdown],
                    outputs=[job_result, job_identifier, job_is_saved, save_job_btn, save_job_status],
                )

                save_job_btn.click(
                    fn=save_job,
                    inputs=[job_result, job_identifier, job_is_saved],
                    outputs=[save_job_status, job_list, job_is_saved, save_job_btn],
                )

                refresh_jobs_btn.click(fn=load_jobs, outputs=[job_list, job_list_dropdown])

                # Load jobs on startup
                app.load(fn=load_jobs, outputs=[job_list, job_list_dropdown])

            # Tab 2: Curriculum Vitae
            with gr.Tab("Curriculum Vitae"):
                with gr.Group():
                    gr.Markdown("### Import CV")
                    cv_file = gr.File(label="CV File", file_types=[".json", ".yaml", ".txt"])
                    cv_path = gr.Textbox(
                        label="Or File Path",
                        placeholder="/path/to/cv.json",
                    )
                    analyze_cv_btn = gr.Button("Analyze CV", variant="primary")

                with gr.Group():
                    gr.Markdown("### Results")
                    cv_result = gr.JSON(label="CV Details")
                    cv_identifier = gr.Textbox(
                        label="Save As",
                        placeholder="name",
                    )
                    cv_is_saved = gr.State(value=False)
                    save_cv_btn = gr.Button("Save CV")
                    save_cv_status = gr.Textbox(label="Status", interactive=False)

                with gr.Group():
                    gr.Markdown("### Saved CVs")
                    cv_list_dropdown = gr.Dropdown(
                        label="Select CV to View",
                        choices=[],
                        interactive=True,
                    )
                    view_cv_btn = gr.Button("View Selected")
                    cv_list = gr.Dataframe(
                        headers=["Identifier", "Name", "Profession"],
                        label="All CVs",
                    )
                    refresh_cvs_btn = gr.Button("Refresh List")

                # Event handlers for CV tab
                def analyze_cv(file, path):
                    file_path = file.name if file else path
                    if not file_path:
                        return None, "", False, gr.update(interactive=False)

                    result = service.create_cv(file_path)
                    identifier = result.get("identifier", "")
                    is_saved = False
                    return result, identifier, is_saved, gr.update(interactive=True)

                def view_saved_cv(identifier):
                    if not identifier:
                        return None, "", True, gr.update(interactive=False), ""

                    cv = service.repository.get_cv(identifier)
                    if not cv:
                        return None, "", True, gr.update(interactive=False), "⚠ CV not found"

                    result = cv.model_dump()
                    result["identifier"] = identifier
                    result["status"] = "loaded"
                    is_saved = True

                    return result, identifier, is_saved, gr.update(interactive=False), f"✓ Loaded: {identifier}"

                def save_cv(cv_data, identifier, is_saved):
                    if is_saved:
                        return "ℹ CV is already saved", None, True, gr.update(interactive=False)

                    if not cv_data or not identifier:
                        return "⚠ Please analyze a CV first and provide an identifier", None, False, gr.update(interactive=True)

                    try:
                        metadata = service.save_cv(cv_data, identifier)
                        cvs = service.get_cvs()
                        cv_list_data = [
                            [c.get("identifier", ""), c.get("name", ""), c.get("profession", "")]
                            for c in cvs
                        ]
                        return (
                            f"✓ CV saved: {metadata['identifier']}",
                            cv_list_data,
                            True,
                            gr.update(interactive=False),
                        )
                    except Exception as e:
                        return f"✗ Error saving CV: {str(e)}", None, False, gr.update(interactive=True)

                def load_cvs():
                    cvs = service.get_cvs()
                    cv_list_data = [
                        [c.get("identifier", ""), c.get("name", ""), c.get("profession", "")]
                        for c in cvs
                    ]
                    cv_choices = [(f"{c['name']} ({c['profession']})", c['identifier']) for c in cvs]
                    return cv_list_data, gr.update(choices=cv_choices)

                analyze_cv_btn.click(
                    fn=analyze_cv,
                    inputs=[cv_file, cv_path],
                    outputs=[cv_result, cv_identifier, cv_is_saved, save_cv_btn],
                )

                view_cv_btn.click(
                    fn=view_saved_cv,
                    inputs=[cv_list_dropdown],
                    outputs=[cv_result, cv_identifier, cv_is_saved, save_cv_btn, save_cv_status],
                )

                save_cv_btn.click(
                    fn=save_cv,
                    inputs=[cv_result, cv_identifier, cv_is_saved],
                    outputs=[save_cv_status, cv_list, cv_is_saved, save_cv_btn],
                )

                refresh_cvs_btn.click(fn=load_cvs, outputs=[cv_list, cv_list_dropdown])

                # Load CVs on startup
                app.load(fn=load_cvs, outputs=[cv_list, cv_list_dropdown])

            # Tab 3: Optimizations
            with gr.Tab("Optimizations"):
                with gr.Group():
                    gr.Markdown("### Create New Optimization")

                    job_dropdown = gr.Dropdown(
                        label="Select Job Posting",
                        choices=[],
                        interactive=True,
                    )
                    cv_dropdown = gr.Dropdown(
                        label="Select CV",
                        choices=[],
                        interactive=True,
                    )
                    optimize_btn = gr.Button("Optimize CV", variant="primary")

                with gr.Group():
                    gr.Markdown("### Progress")
                    optimization_status = gr.Textbox(
                        label="Status",
                        interactive=False,
                        value="Ready to optimize",
                    )

                with gr.Group():
                    gr.Markdown("### Results")
                    optimization_result = gr.JSON(label="Optimization Details")

                with gr.Group():
                    gr.Markdown("### Saved Optimizations")
                    optimization_list = gr.Dataframe(
                        headers=["Identifier", "Job Posting", "CV", "Date"],
                        label="Optimizations",
                    )
                    refresh_optimizations_btn = gr.Button("Refresh List")

                # Event handlers for Optimizations tab
                def load_job_choices():
                    jobs = service.get_job_postings()
                    return gr.Dropdown(
                        choices=[(f"{j['company']} - {j['title']}", j["identifier"]) for j in jobs]
                    )

                def load_cv_choices():
                    cvs = service.get_cvs()
                    return gr.Dropdown(
                        choices=[(f"{c['name']} ({c['profession']})", c["identifier"]) for c in cvs]
                    )

                def run_optimization(job_id, cv_id):
                    if not job_id or not cv_id:
                        return "⚠ Please select both a job posting and a CV", {}

                    result = service.create_optimization(job_id, cv_id)
                    status = f"✓ Optimization complete: {result.get('identifier', '')}"
                    return status, result

                def load_optimizations():
                    opts = service.get_optimizations()
                    return [
                        [
                            o.get("identifier", ""),
                            o.get("job_posting", ""),
                            o.get("cv", ""),
                            o.get("date", ""),
                        ]
                        for o in opts
                    ]

                optimize_btn.click(
                    fn=run_optimization,
                    inputs=[job_dropdown, cv_dropdown],
                    outputs=[optimization_status, optimization_result],
                )

                refresh_optimizations_btn.click(fn=load_optimizations, outputs=[optimization_list])

                # Load optimizations and choices on startup
                app.load(fn=load_job_choices, outputs=[job_dropdown])
                app.load(fn=load_cv_choices, outputs=[cv_dropdown])
                app.load(fn=load_optimizations, outputs=[optimization_list])

            # Tab 4: PDF Generation
            with gr.Tab("PDF Generation"):
                with gr.Group():
                    gr.Markdown("### Generate PDF")

                    optimization_dropdown = gr.Dropdown(
                        label="Select Optimization",
                        choices=[],
                        interactive=True,
                    )

                    gr.Markdown("Or upload CV JSON:")
                    cv_json_file = gr.File(label="CV JSON File", file_types=[".json"])

                    template_dropdown = gr.Dropdown(
                        label="Template",
                        choices=["cv.tex", "cover-letter.tex"],
                        value="cv.tex",
                    )

                    generate_pdf_btn = gr.Button("Generate PDF", variant="primary")

                with gr.Group():
                    gr.Markdown("### Result")
                    pdf_status = gr.Textbox(label="Status", interactive=False)
                    pdf_download = gr.File(label="Download PDF", interactive=False)

                # Event handlers for PDF tab
                def load_optimization_choices():
                    opts = service.get_optimizations()
                    return gr.Dropdown(
                        choices=[
                            (f"{o['job_posting']} - {o['date']}", o["identifier"])
                            for o in opts
                        ]
                    )

                def generate_pdf(optimization_id, cv_json, template):
                    if not optimization_id and not cv_json:
                        return "⚠ Please select an optimization or upload a CV JSON", None

                    result = service.generate_pdf(optimization_id)
                    status = f"✓ PDF generated: {result.get('pdf_path', '')}"
                    # TODO: Actually return the PDF file for download
                    return status, None

                generate_pdf_btn.click(
                    fn=generate_pdf,
                    inputs=[optimization_dropdown, cv_json_file, template_dropdown],
                    outputs=[pdf_status, pdf_download],
                )

                # Load optimization choices on startup
                app.load(fn=load_optimization_choices, outputs=[optimization_dropdown])

    return app


def launch():
    """Launch the Gradio application."""
    app = create_app()
    app.launch(inbrowser=True)
