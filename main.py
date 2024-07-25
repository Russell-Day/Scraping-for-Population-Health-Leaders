import pandas as pd
import utils.accessing_web as web
import utils.llama70 as cl70
import utils.gemini15 as g15
import time
import concurrent.futures

# reads in the pubmed ids
hospital_name_df = pd.read_csv("AcuteHospitalList.csv", usecols=["NAME"])

print(hospital_name_df)

# takes those pubmed ids and puts it into a 
hospital_list = hospital_name_df["NAME"].tolist()[800:900]

# different variables that want to be accounted for
hospital_name = []
search = [
    {"title": [], "link": [], "pop_health": []},
    {"title": [], "link": [], "pop_health": []},
    {"title": [], "link": [], "pop_health": []},
]

#title, first author, year of publication, citation, link, summary, sentiments 
output_dict = {
    "Hospital Name": hospital_name,
    "Title 1": search[0]["title"],
    "Link 1": search[0]["link"],
    "Population Health 1": search[0]["pop_health"],
    "Title 2": search[1]["title"],
    "Link 2": search[1]["link"],
    "Population Health 2": search[1]["pop_health"],
    "Title 3": search[2]["title"],
    "Link 3": search[2]["link"],
    "Population Health 3": search[2]["pop_health"],
}
api_num = 0
run_num = 0
start_time = time.time()

for hospitals in hospital_list:
    hospital_name.append(hospitals)

    # query {hospital} health population leaders
    query_results = web.get_web_results(f"{hospitals} population health leaders", api_num)
    
    for i in range(3):
        search[i]["title"].append(query_results[i]["title"])
        search[i]["link"].append(query_results[i]["link"])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        hospital_1_future = executor.submit(g15.get_health_leaders, query_results[0]["link"], api_num)
        api_num += 1
        hospital_2_future = executor.submit(g15.get_health_leaders, query_results[1]["link"], api_num)
        api_num += 1
        hospital_3_future = executor.submit(g15.get_health_leaders, query_results[2]["link"], api_num)
        api_num += 1
    
    search[0]["pop_health"].append(hospital_1_future.result())
    search[1]["pop_health"].append(hospital_2_future.result())
    search[2]["pop_health"].append(hospital_3_future.result())

    df = pd.DataFrame(output_dict)
    df.to_csv("streaming.csv")

    run_num += 1
    print(f"Run number: {run_num}, Time: {time.time() - start_time}, Hospital: {hospitals}")



df = pd.DataFrame(output_dict)
df.to_excel("output.xlsx")

print(time.time() - start_time)