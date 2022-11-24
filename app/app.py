from flask import Flask, render_template, request, redirect, send_file,Response
from extractor.indeed_extractor import ExtractIndeed
import pandas as pd

# from file import save_to_file

app = Flask(__name__)




@app.route("/")
def home():
    return render_template("home.html", name="JJ")


@app.route("/search")
def search():
    web = request.form.get("web")
    tech = request.form.get("tech")
    print(web,tech)

    if web == None or tech == None:
        return redirect("/")
    
    scrap_naukri = ExtractIndeed(tech)
    data = scrap_naukri.scrap_details()
    scrap_naukri.generate_csv()

    company_name = data["company_name"]
    location =data['location']
  
            
    # print(description_list, company_name_list, designation_list, salary_list, company_url,location_list, qualification_list)

    return render_template("search.html",company_name=company_name,location=location)



@app.route("/export")
def export():
    # return send_file(pd.read_csv('indeed_jobs_python.csv'),download_name='logo.png',
    #  as_attachment=True,mimetype="text/csv")

    # csv = pd.read_csv('indeed_jobs_python.csv')
    import os
    csv_dir = "./static"
    csv_file = 'indeed_jobs_python.csv'
    csv_path = os.path.join(csv_dir,csv_file)
    return send_file(
        csv_path,as_attachment=True
    )
    return Response(
        csv_path,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=indeed_jobs_python.csv"})

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)
