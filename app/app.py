from flask import Flask, render_template, request, redirect, send_file
from extractor.indeed_extractor import ExtractIndeed

# from file import save_to_file

app = Flask(__name__)




@app.route("/")
def home():
    return render_template("home.html", name="JJ")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    print('------',keyword)
    if keyword == None:
        return redirect("/")
    scrap_naukri = ExtractIndeed(keyword)
    data = scrap_naukri.scrap_details()
    company_name = data["company_name"]
    location = data['location']
  
            
    # print(description_list, company_name_list, designation_list, salary_list, company_url,location_list, qualification_list)

    return render_template("search.html",company_name=company_name,location=location)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")

    if keyword == None:
        return redirect("/")

    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    save_to_file(keyword, db[keyword])

    return send_file(f"{keyword}.csv", as_attachment=True)

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)
