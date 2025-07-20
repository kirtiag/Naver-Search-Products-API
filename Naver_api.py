import random,os,requests
import time,math,re
import urllib.parse 

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("Flask not found. Installing...")
    os.system("pip install Flask")
    from flask import Flask,request, jsonify
    
try:
    from fake_useragent import UserAgent
except ImportError:
    print("UserAgent not found. Installing...")
    os.system("pip install fake_useragent")
    from fake_useragent import UserAgent 
    
import Crentials

app = Flask(__name__)
ua = UserAgent()

# Optional: Your proxy list here
PROXYEMPIREUSERNAME = Crentials.username
PROXYEMPIREPASSWORD = Crentials.password
PROXYEMPIREPROXY = "rotating.proxyempire.io"
port = str(random.randint(9000, 9999))

def fetch_page(query_url,page_size):
    PROXIES = {
        "http": f"http://{PROXYEMPIREUSERNAME}:{PROXYEMPIREPASSWORD}@{PROXYEMPIREPROXY}:{port}",
        "https": f"http://{PROXYEMPIREUSERNAME}:{PROXYEMPIREPASSWORD}@{PROXYEMPIREPROXY}:{port}",
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': 'https://search.shopping.naver.com/ns/search?query=iphone',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Cookie': 'nstore_session=+mnfG//dhs+3gE/Qu2DPyMxl; sus_val=cNJQGvGWtkXElbccyEB88yxB; X-Wtm-Cpt-Tk=ffSp83A8V6SVqvbqP-PD4oWU81wnOEcJr4vYBb02Cg8lgwcGxbmlAfUu9Qd2cxUUUlzsn80hbM4Kx1B6gQ_Yu9Bmd4ejeUXZx_L0jsSZhJ215OcAsLGNoh6Kk25SJXFTKxdoYJEq5t-4b1AcehpRE5W4I1DiEEz0jbLCtJJe5SPkRJKT96ucs2mWPk-ophXeVT2kvO2u_QHy53A2D6mvdOebPQyjIAAHjEXvSOssooFt9mMHF7ZITAvmN44zJXPyKoyJWplOMU_UNWTCLrAe7hn284R15gEzKssjGHKbi9IHqnGZUoIMFmWOdFsplDsDmpj_MkS9Ey21oJiuYzjntdOyr9Ix5NsBBaCfs4M=; nstore_pagesession=jcFFhdqr62b38wsL9Pw-089429; RELATED_PRODUCT=ON; SRT30=1752819557; SRT5=1752819557; BUC=pgIvs0wf_xVLFlkvaKCKbuCDgc-Iv6GsVgKDWfTK5os=; NNB=EBBO5SDF454WQ; nstore_session=+mnfG//dhs+3gE/Qu2DPyMxl',
    }
 
    try:
        # if page_size > 100:
        pagination   = math.ceil(page_size/100)
        match        = re.search(r'cursor=([^&]+)', query_url)
        if match:
            cursor_value = match.group(1)
        all_results = []
        total_time = 0
        
        for i in range(pagination):
            new_cursor   = int(cursor_value) + (i * 100)
            page_limit   = 100
            modified_url = re.sub(r'pageSize=\d+', f'pageSize={page_limit}', query_url)
            updated_url  = re.sub(r'cursor=[^&]*', f'cursor={new_cursor}', modified_url)
            start = time.time()
            response = requests.get(updated_url, headers=headers, proxies=PROXIES)
            time.sleep(random.uniform(0.5, 1.5))
            duration = time.time() - start
            total_time += duration
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'data' in data['data']:
                    all_results.extend(data['data']['data'])
                else:
                    print(f"[-] Unexpected response structure at page {i+1}")
                    break
            elif response.status_code == 418:
                
                print(f"[Page {i+1}] return 418 HTTP. Retrying once...")
                time.sleep(random.uniform(1, 3))
                retry_start = time.time()
                response_retry = requests.get(updated_url, headers=headers, proxies=PROXIES)
                retry_duration = time.time() - retry_start
                total_time += retry_duration
                if response_retry.status_code == 200:
                    data = response_retry.json()
                    if 'data' in data and 'data' in data['data']:
                        all_results.extend(data['data']['data'])
                    else:
                        print(f"[-] Unexpected response structure on retry at page {i+1}")
                        
                        return None
                else:
                    print(f"[Page {i+1}] Still blocked after retry with status {response_retry.status_code}. Skipping this page.")
                    
                    continue      
            else:
                print(f"[-] Error fetching page {i+1}: {response.status_code}")
                break
        if pagination > 0:
            average_latency = total_time / pagination
            print(f"\n✅ Average latency per page: {average_latency:.2f} seconds")
        return {"data": {"data": all_results}} if all_results else None

    except Exception as e:
        print(f"Error: {e}")
        return None


def scrape_products(query_url,page_size):
    # Fetch the page data
    data = fetch_page(query_url,page_size)
    
    if not data:
        return None

    collected = []
    for card in data['data']['data']:
        items = card['card']['product']
        product = {
            "product_name": items['productName'],
            "price": items['salePrice'],
            "product_url": items['productUrl']['pcUrl'],
        }
        if all(product.values()):
            collected.append(product)

    return collected[:page_size]

# REST API endpoint
@app.route("/naver", methods=["GET"])
def get_products():
    # query_url = request.args.get('query_url')
    
    query_url = '&'.join([f"{k}={v}" for k,v in request.args.items()]).replace('query_url=','')
    page_size = int(request.args.get("pageSize", 100))
    MAX_PAGE_SIZE = 1000
    if page_size > MAX_PAGE_SIZE:
        return jsonify({
            "error": f"Maximum allowed pageSize is {MAX_PAGE_SIZE}"
        }), 400
    results = scrape_products(query_url,page_size)

    if not results:
        return jsonify({"error": "Failed to retrieve data"}), 500

    return jsonify({"total": len(results), "products": results})

if __name__ == "__main__":
    app.run(debug=True, port=5000)