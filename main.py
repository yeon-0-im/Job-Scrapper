from flask import Flask, render_template, request, redirect
from extractors.wwr import extract_wwr_jobs
from extractors.webs import extract_webs_jobs
from extractors.berlinstarupjobs import extract_bs_jobs
from file import save_to_file

app = Flask('JobScrapper')

@app.route('/')
def home():
    return render_template("home.html", name='nico')

db = { }

@app.route('/search')
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect('/')
    if keyword in db:
        jobs = db[keyword]
    else:
        webs = extract_webs_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        bsj = extract_bs_jobs(keyword)
        jobs = wwr + webs + bsj
        db[keyword] = jobs
    return render_template("search.html", keyword = keyword, jobs = jobs)

app.run("0.0.0.0")
save_to_file(keyward, jobs)