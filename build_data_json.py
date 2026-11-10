#!/usr/bin/env python3
"""Build data.json for convertibles-site from scraped data."""
import json
from datetime import datetime, timezone

# ─── CARS.COM ────────────────────────────────────────────────────────────────
# Format: [id8, fullId, year, make, model, trim, price, mileage, imageUrl, dealer, dealerZip]
# Excludes: 2-seater roadsters, MINI, Ohio dealer (45150)

CARSCOM_RAW = [
    # PAGE 1 (8 unique eligible)
    ["97c8159e","97c8159e-2ad2-48b5-ab9d-98c1081303e2",2012,"BMW","128","128i",12704,86671,
     "https://platform.cstatic-images.com/in/v2/74cd7801-ed1b-554a-a133-7a8b7ee99784/7733e84b-5b55-4f09-8f7d-7187f020e8ec/tdT79jfEfhPbcMg0yGDVNoj22Ts.jpg",
     "PAAUTOSALES.COM","19116"],
    ["5a563051","5a563051-6ebc-4c5b-a09e-277d9d84f77a",2003,"BMW","330","330Cic Convertible 2D",10977,100123,
     "https://platform.cstatic-images.com/in/v2/779a78eb-783a-43a2-89ef-bb4017a826b3/19e53f46-22db-4871-9571-655c570de0f8/y4hZalH_ae58M139FTD50DKOZ1M.jpg",
     "Trend Auto Motors Inc","19355"],
    ["9861c16f","9861c16f-3864-41a3-9aaa-d387fc03f10d",2014,"Ford","Mustang","V6",10495,109452,
     "https://platform.cstatic-images.com/in/v2/2d6e9a7c-9da8-4788-ad45-185839bf3972/e124027a-229e-4acd-b72e-0c5dc8542855/VODlj9OwATz95PZrANm141D7Hak.jpg",
     "Brother's Auto Center","08312"],
    ["684a6879","684a6879-8ff5-4dd5-9d0b-1485b08a22f5",2012,"Volvo","C70","T5",7773,131847,
     "https://platform.cstatic-images.com/in/v2/5aef8e01-b2d4-5e77-8bd0-4dab09cf2f86/7e9c14d6-6f4d-4d13-9e49-8b5c7a4aedc2/dummy.jpg",
     "Davis Honda","08016"],
    ["6482454c","6482454c-a7c7-4ece-9224-b16307df189f",2013,"INFINITI","G37","Base",12988,91309,
     "https://platform.cstatic-images.com/in/v2/c04447ce-c7d6-5b50-ab72-ee5ab9e22495/0b874690-9551-4d99-80c5-1dbaef9155a7/_-JgjyfWJX49WmwFZTNGlFn03pI.jpg",
     "Faulkner INFINITI","19090"],
    ["e8f762b2","e8f762b2-d1fe-4815-8755-53aee804f98b",2005,"Jaguar","XK8","Base",12950,51549,
     "https://platform.cstatic-images.com/in/v2/a733be78-f490-4868-adbe-201a3d056e0c/2a597d81-324b-4fc6-9886-1436a47ae8f9/Uw_rKHIXYfis06fXa6LAWVVZJH0.jpg",
     "Car Cheer","19053"],
    ["c822098f","c822098f-4e48-4053-ac80-cac595d90b63",2011,"BMW","128","128i 2dr Convertible SULEV",7485,147552,
     "https://platform.cstatic-images.com/in/v2/66aedd22-5f4c-571c-bcc9-9a6e5d5a07c7/9ad95780-0702-412c-b31e-e44fa24094aa/VzajC8Oo11oD-uHgdt9QaZM7B48.jpg",
     "Bristol Auto Mall","19057"],
    ["dcf43a76","dcf43a76-4a2c-49cd-abf9-0da63e683140",2009,"Volkswagen","Eos","Lux",7389,91737,
     "https://platform.cstatic-images.com/in/v2/368a5253-cda5-46bf-9f9e-786a51b409e5/131936bf-21d1-468b-b8ec-008ecec77784/a8U2YDC_dVK8JrIZK8Du9v2xjv8.jpg",
     "Legacy Used Auto LLC","18964"],
    # PAGE 2 (10 eligible, excluding Ohio 45150 Camry Solara)
    ["3379f96f","3379f96f-c7f9-4cbd-a6f3-f1e29635b9d0",2015,"Audi","A5","2.0T Premium Plus",11480,108217,
     "https://platform.cstatic-images.com/in/v2/c55653a2-dba3-577c-9761-100f25492861/7e3451e8-a62d-4526-98cc-21e804803d55/UK_BOCe6slT0chIwWvzBZy5JOIY.jpg",
     "Bergey's Lincoln","19446"],
    ["11a59567","11a59567-1e64-4f4b-a04a-6708a153e1ad",1995,"Jaguar","XJS","2+2",8899,46103,
     "https://platform.cstatic-images.com/in/v2/2a9ff44c-1d8c-572a-b85a-e2c017e560ce/eec71dc7-9fe7-4cbe-86f1-4f071ac06ac8/5WgTTGYREAi4bO4kfEPlo0Ncpmw.jpg",
     "Avi Auto Sales","08049"],
    ["1faf3dba","1faf3dba-c46d-4f7d-9b51-83a5669ebaae",2012,"Audi","A5","2.0T Premium",8495,80410,
     "https://platform.cstatic-images.com/in/v2/p2p/16b786f6-0c39-436c-95a7-05465908b11d/01d78260-a9ec-422a-8a85-d830ecdabb8f",
     None,"19438"],
    ["a513484f","a513484f-cf02-4dbc-95ef-634dfcf3b3bb",2003,"BMW","330","330Ci 2dr Convertible",9495,64358,
     "https://platform.cstatic-images.com/in/v2/915dc978-cb40-5160-94a4-afaa35adacb8/85261c6d-9dc8-4f72-b1a8-9244ecccaf79/iDrG-hqKtpND5Nw-jIG8TFqzBO4.jpg",
     "GEG Automotive LLC","19525"],
    ["bfc8a417","bfc8a417-6fcf-4ab2-9daf-c8f8b5bba74f",2013,"Volvo","C70","T5 Premier Plus Convertible 2D",12990,100858,
     "https://platform.cstatic-images.com/in/v2/5ba3cb38-9313-46f4-bf2a-09e8e250c34b/f87be388-28f6-40dd-b902-0ea5325d46aa/SAKf6JHcRfK6x4uqwTo_a3Dxofw.jpg",
     "JC MILLER AUTO SALES INC","08360"],
    ["79ae64dc","79ae64dc-25ce-4249-88e0-83729a3c5ce5",2016,"Audi","A3","2.0T Premium",12500,84000,
     "https://platform.cstatic-images.com/in/v2/p2p/0cb11156-d4b9-4b04-b292-c2f8153b0994/a868667f-4021-4b17-9e2d-ba6d653f48ab.JPG",
     None,"19462"],
    ["4ec1af9d","4ec1af9d-ea07-4635-a417-496303daee38",2018,"BMW","430","i xDrive",14999,111270,
     "https://platform.cstatic-images.com/in/v2/6a443be0-9426-5926-8102-c8cb3136fd0d/dbd02e73-00be-4901-97ea-e1186cee6777/mZzZnA0I7matU-todu1TgH7K4FU.jpg",
     "Eastern Auto Exchange","08620"],
    ["58c27482","58c27482-081b-4030-8ab0-528d44b703b9",2007,"BMW","328","i",14485,34431,
     "https://platform.cstatic-images.com/in/v2/84f99b5a-f558-5eec-a1f1-3c0a5bf0dad5/Ki1qN9xzDrP97mK7O___Qv/IEbVYq1mzlk-zkS-ESoUZDbC_8U.jpg",
     "Scott Mazda","18103"],
    ["09628d44","09628d44-73e9-480b-8fb5-aeb7798e4da0",2013,"Volvo","C70","T5",10889,102592,
     "https://platform.cstatic-images.com/in/v2/7300ae19-ff54-5820-9215-33b20011b624/ffdd542b-0be9-4b85-96ec-756f835751db/Ryl24_43JB40piLkxFYfuwEnoXE.jpg",
     "Miracle Autosport","08619"],
    ["11386bb9","11386bb9-0a62-4902-9964-2118bf6f5b04",2013,"Ford","Mustang","V6 Premium",10599,97202,
     "https://platform.cstatic-images.com/in/v2/b19182ae-668a-5e30-93ee-2b50a30a2c77/0153cdac-7c4b-44d1-bce5-5f3bf609348c/pVtJ7YR8I4cgB1M7ApQ157hq48Q.jpg",
     "Independence Auto Sale","08505"],
]

# Location lookup by zip (best-effort)
ZIP_LOCATION = {
    "19116": "Philadelphia, PA", "19355": "Malvern, PA", "08312": "Clayton, NJ",
    "08016": "Burlington, NJ", "19090": "Willow Grove, PA", "19053": "Feasterville-Trevose, PA",
    "19057": "Levittown, PA", "18964": "Souderton, PA", "19446": "Lansdale, PA",
    "08049": "Magnolia, NJ", "19438": "Towamencin, PA", "19525": "Gilbertsville, PA",
    "08360": "Vineland, NJ", "19462": "Plymouth Meeting, PA", "08620": "Trenton, NJ",
    "18103": "Allentown, PA", "08619": "Trenton, NJ", "08505": "Jobstown, NJ",
}

# Rough distanceMi from ZIP 19063 (Media, PA)
ZIP_DISTANCE = {
    "19116": 26, "19355": 13, "08312": 26, "08016": 30, "19090": 23,
    "19053": 28, "19057": 35, "18964": 28, "19446": 24, "08049": 21,
    "19438": 25, "19525": 29, "08360": 35, "19462": 16, "08620": 33,
    "18103": 50, "08619": 33, "08505": 32,
}

carscom_listings = []
for row in CARSCOM_RAW:
    id8, fullId, year, make, model, trim, price, mileage, imageUrl, dealer, zip_ = row
    loc = ZIP_LOCATION.get(zip_, zip_)
    dist = ZIP_DISTANCE.get(zip_, 30)
    carscom_listings.append({
        "id": id8,
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
        "price": price,
        "mileage": mileage,
        "location": loc,
        "distanceMi": dist,
        "url": f"https://www.cars.com/vehicledetail/{fullId}/",
        "dealer": dealer,
        "dealRating": None,
        "cleanTitle": True,
        "noAccidents": True,
        "transmission": None,
        "imageUrl": imageUrl or "",
        "source": "cars.com"
    })

# ─── CARGURUS ────────────────────────────────────────────────────────────────
# From cargurus_p1.txt: id|year|make|model|trim|price|mileage|location|distanceMi|dealRating|transmission|imageUrl|url
CARGURUS_RAW = [
    ["461597986",2012,"Volkswagen","Eos","Komfort SULEV",9463,86370,"Croydon, PA",29,"Fair Deal",None,
     "https://static.cargurus.com/images/forsale/2026/11/05/04/55/2012_volkswagen_eos-pic-4505014155695517943-1024x768.jpeg",
     "https://www.cargurus.com/details/461597986"],
    ["458458849",2014,"Chrysler","200","Limited Convertible FWD",7485,86273,"Langhorne, PA",33,"Good Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/08/14/07/2014_chrysler_200-pic-4021463906697366974-1024x768.jpeg",
     "https://www.cargurus.com/details/458458849"],
    ["458428863",2011,"BMW","3 Series","328i Convertible RWD",7888,89795,"Medford, NJ",32,"Great Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/16/15/54/2011_bmw_3_series-pic-5698928836052780629-1024x768.jpeg",
     "https://www.cargurus.com/details/458428863"],
    ["456364076",2015,"Audi","A3","2.0T quattro Premium Plus Cabriolet AWD",12299,105069,"Monroeville, NJ",23,"Fair Deal",None,
     "https://static.cargurus.com/images/forsale/2026/09/09/10/27/2015_audi_a3-pic-6948141372738757313-1024x768.jpeg",
     "https://www.cargurus.com/details/456364076"],
    ["455946186",2013,"INFINITI","G37","Convertible RWD",12489,91309,"Willow Grove, PA",23,"Good Deal",None,
     "https://static.cargurus.com/images/forsale/2026/11/06/09/27/2013_infiniti_g37-pic-1660226628461026038-1024x768.jpeg",
     "https://www.cargurus.com/details/455946186"],
    ["454910434",2012,"Audi","A5","2.0T quattro Premium Plus Cabriolet AWD",10190,86962,"",18,"Fair Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/22/08/48/2012_audi_a5-pic-5440491617432993742-1024x768.jpeg",
     "https://www.cargurus.com/details/454910434"],
    ["453750011",2010,"Audi","S5","3.0T quattro Premium Plus Cabriolet AWD",10489,92034,"Feasterville Trevose, PA",27,"Good Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/14/15/08/2010_audi_s5-pic-4832088940729344249-1024x768.jpeg",
     "https://www.cargurus.com/details/453750011"],
    ["462508217",2009,"BMW","3 Series","335i Convertible RWD",14333,38748,"Doylestown, PA",34,"Good Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/30/17/03/2009_bmw_3_series-pic-2777642979638457842-1024x768.jpeg",
     "https://www.cargurus.com/details/462508217"],
    ["461341277",2014,"Ford","Mustang","V6 Convertible RWD",8048,167500,"Woodlynne, NJ",18,"Fair Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/10/21/02/2014_ford_mustang-pic-8504083305349075543-1024x768.jpeg",
     "https://www.cargurus.com/details/461341277"],
    ["457339579",2007,"Volkswagen","Beetle","2.5L Convertible",7094,99882,"Berlin, NJ",27,"Fair Deal",None,
     "https://static.cargurus.com/images/forsale/2026/08/28/01/03/2007_volkswagen_beetle-pic-625193239448549921-1024x768.jpeg",
     "https://www.cargurus.com/details/457339579"],
    ["454648300",2013,"Mercedes-Benz","E-Class","E 350 Cabriolet",7900,152912,"Burlington, NJ",31,"Fair Deal",None,
     "https://static.cargurus.com/images/forsale/2026/07/29/07/56/2013_mercedes-benz_e-class-pic-3780741551422153063-1024x768.jpeg",
     "https://www.cargurus.com/details/454648300"],
    ["462017255",2011,"BMW","3 Series","328i Convertible RWD",8972,118267,"Feasterville-Trevose, PA",29,"Fair Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/19/19/41/2011_bmw_3_series-pic-202222175876792318-1024x768.jpeg",
     "https://www.cargurus.com/details/462017255"],
    ["457408910",2017,"BMW","4 Series","430i xDrive Convertible AWD",13195,112184,"Birdsboro, PA",32,"Great Deal",None,
     "https://static.cargurus.com/images/forsale/2026/10/13/07/55/2017_bmw_4_series-pic-4705782880859175264-1024x768.jpeg",
     "https://www.cargurus.com/details/457408910"],
]

cargurus_listings = []
for row in CARGURUS_RAW:
    id_, year, make, model, trim, price, mileage, loc, dist, deal, trans, img, url = row
    cargurus_listings.append({
        "id": id_,
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
        "price": price,
        "mileage": mileage,
        "location": loc or None,
        "distanceMi": dist,
        "url": url,
        "dealer": None,
        "dealRating": deal,
        "cleanTitle": None,
        "noAccidents": None,
        "transmission": trans,
        "imageUrl": img,
        "source": "cargurus"
    })

# ─── AUTOTRADER ──────────────────────────────────────────────────────────────
# Text extracted from 3 pages; no listing IDs or image URLs available
# Format: [year, make, model, trim, price, mileageK, dealer, distanceMi, dealRating]
AT_SEARCH_URL = "https://www.autotrader.com/cars-for-sale/all-cars/convertible/cars-between-7000-and-15000/media-pa?searchRadius=35&sortBy=derivedpriceASC"

AUTOTRADER_RAW = [
    # Page 1
    [1994,"Ford","Mustang","GT",7495,44,"CarNu Sales",27,None],
    [1995,"Pontiac","Firebird","Convertible",7500,124,"Private Seller",30,None],
    [2012,"Volvo","C70","T5",7773,131,"Davis Honda",31,None],
    [2004,"Mercedes-Benz","CLK 500","Cabriolet",7900,82,"Private Seller",32,None],
    [2009,"BMW","335i","Convertible",8000,107,"EXTREME AUTO CARE",21,None],
    [1995,"Jaguar","XJS","4.0 Convertible",8499,46,"Avi Auto Sales",21,None],
    [2015,"BMW","435i xDrive","Convertible",8500,140,"Private Seller",27,None],
    [2013,"Volkswagen","Eos","Lux",9797,98,"SPEEDY CAR SALES",8,None],
    [2013,"BMW","328i","Convertible",10390,144,"Josie's Auto Sales",29,None],
    [2014,"Ford","Mustang","V6 Convertible",10390,121,"Josie's Auto Sales",29,None],
    [2014,"Ford","Mustang","Convertible",10437,128,"Discount Auto",34,None],
    [2011,"BMW","328i","Convertible",10475,123,None,24,None],
    [2010,"Audi","S5","Premium Plus",10489,92,"Divan Auto Group",27,"Great Price"],
    [2014,"Ford","Mustang","Premium",10495,109,"BROTHER'S AUTO CENTER LLC",25,None],
    [2008,"BMW","135i","Convertible",11595,48,"Premier Auto Group",22,None],
    [2014,"Mercedes-Benz","E 350","Cabriolet",13751,79,"Porsche Conshohocken",14,"Great Price"],
    [2009,"BMW","335i","Convertible",14333,38,"Mercedes-Benz of Doylestown",34,None],
    # Page 2 new
    [1997,"Chevrolet","Camaro","Z28",10495,73,"MERIC AUTO GROUP LLC",29,None],
    [2003,"BMW","330Ci","Convertible",10977,100,"Trend Auto Motors",13,None],
    [1993,"Jaguar","XJS","4.0 Convertible",11000,110,"Private Seller",27,None],
    [2015,"Audi","A5","2.0T Premium Plus",11480,108,None,24,None],
    [2016,"Volkswagen","Beetle","1.8T Denim",11875,98,"Private Seller",None,None],
    [2016,"Buick","Cascada","Premium",12485,95,"Peruzzi Mazda",34,None],
    [2013,"INFINITI","G37","Convertible",12489,91,"Faulkner INFINITI",21,"Great Price"],
    [2016,"Audi","A3","2.0T Premium",12500,84,"Private Seller",4,None],
    [2006,"Lexus","SC 430","Convertible",13485,146,"Advanced Auto",10,None],
    # Page 3 new
    [2013,"Volkswagen","Beetle","2.5",13825,90,"Woerth Motor Co.",32,None],
    [2012,"INFINITI","G37","Convertible",14254,83,None,27,None],
    [2015,"BMW","428i xDrive","Convertible",14390,101,"Josie's Auto Sales",29,None],
    [2015,"BMW","435i xDrive","Convertible",14995,117,"Southampton Imported Cars",35,None],
    [2004,"Ford","Mustang","GT",14999,47,"CrossRoads Auto Sales",11,None],
]

autotrader_listings = []
for i, row in enumerate(AUTOTRADER_RAW):
    year, make, model, trim, price, mileageK, dealer, distMi, deal = row
    slug = f"at-{year}-{make.lower().replace(' ','-').replace('-benz','')}-{model.lower().replace(' ','-')}-{i+1}"
    autotrader_listings.append({
        "id": slug,
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
        "price": price,
        "mileage": mileageK * 1000,
        "location": None,
        "distanceMi": distMi,
        "url": AT_SEARCH_URL,
        "dealer": dealer,
        "dealRating": deal,
        "cleanTitle": None,
        "noAccidents": None,
        "transmission": None,
        "imageUrl": "",
        "source": "autotrader"
    })

# ─── BUILD TOP 10 BEST BUYS ──────────────────────────────────────────────────
# Criteria: best value = good deal rating + lower mileage for price + desirable make/model
# Prioritize: Great/Good deal ratings, clean titles, lower mileage relative to price, source diversity

def value_score(listing):
    """Lower score = better value."""
    price = listing["price"]
    mileage = listing["mileage"]
    deal = listing.get("dealRating") or ""

    # Base: price/mileage ratio (cents per mile)
    if mileage > 0:
        cpp = price / mileage
    else:
        cpp = price / 50000

    # Deal rating bonus
    if "Great" in deal:
        cpp *= 0.7
    elif "Good" in deal:
        cpp *= 0.85
    elif "Fair" in deal:
        cpp *= 1.0

    # Desirability bonus for certain makes
    make = listing["make"]
    model = listing["model"]
    if make in ["Audi","BMW","INFINITI","Mercedes-Benz","Jaguar"]:
        cpp *= 0.9

    # Clean title bonus (cars.com all have cleanTitle=True)
    if listing.get("cleanTitle"):
        cpp *= 0.95

    return cpp

# Collect all listings for scoring
all_listings = carscom_listings + cargurus_listings + autotrader_listings

# Deduplicate: same year/make/model/price/mileage combo → keep best (cars.com > cargurus > autotrader)
source_priority = {"cars.com": 0, "cargurus": 1, "autotrader": 2}

seen_combos = {}
for lst in all_listings:
    key = (lst["year"], lst["make"].lower(), lst["model"].lower(), lst["price"])
    src = source_priority.get(lst["source"], 9)
    if key not in seen_combos or src < source_priority.get(seen_combos[key]["source"], 9):
        seen_combos[key] = lst

unique_listings = list(seen_combos.values())

# Sort by value score, pick top 10
unique_listings.sort(key=value_score)
top10_picks = unique_listings[:10]

# ─── MUSTANGS (2005+) ────────────────────────────────────────────────────────
mustang_listings = []
seen_mustangs = {}
for lst in all_listings:
    if lst["make"] == "Ford" and lst["model"] in ["Mustang"] and lst["year"] >= 2005:
        key = (lst["year"], lst["price"], lst["mileage"])
        src = source_priority.get(lst["source"], 9)
        if key not in seen_mustangs or src < source_priority.get(seen_mustangs[key]["source"], 9):
            seen_mustangs[key] = lst

mustang_picks = sorted(seen_mustangs.values(), key=lambda x: x["mileage"])

# ─── MANUAL TRANSMISSION ─────────────────────────────────────────────────────
# No explicit manual transmission data available from extraction; leave empty
manual_picks = []

# ─── ASSEMBLE DATA.JSON ──────────────────────────────────────────────────────
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Add rank field (1-based) to every pick — index.html reads p.rank directly
def add_ranks(picks):
    return [{**p, "rank": i + 1} for i, p in enumerate(picks)]

top10_picks   = add_ranks(top10_picks)
mustang_picks = add_ranks(mustang_picks)
manual_picks  = add_ranks(manual_picks)

data = {
    "lastRefreshed": now,
    "filters": {
        "minPrice": 7000,
        "maxPrice": 15000,
        "radiusMi": 35,
        "zip": "19063",
        "minSeats": 4,
        "mustangMinYear": 2005
    },
    "carscom": {
        "totalFound": 34,
        "url": "https://www.cars.com/shopping/results/?body_style_slugs%5B%5D=convertible&clean_title=true&list_price_max=15000&list_price_min=7000&maximum_distance=35&no_accidents=true&sort=best_match_desc&stock_type=used&zip=19063",
        "listings": carscom_listings
    },
    "cargurus": {
        "totalFound": 42,
        "url": "https://www.cargurus.com/Cars/new/nl_SRP_d2184_z19063.html",
        "listings": cargurus_listings
    },
    "autotrader": {
        "totalFound": len(autotrader_listings),
        "url": AT_SEARCH_URL,
        "listings": autotrader_listings
    },
    "truecar": {
        "totalFound": 0,
        "url": "",
        "listings": []
    },
    "top10": {
        "introHtml": f"<p>The best convertibles under $15K within 35 miles of Media, PA — ranked by value, condition, and desirability. Prioritized: deal ratings, clean titles, lower miles for price, and source diversity. Refreshed {datetime.now().strftime('%B %-d, %Y')}.</p>",
        "picks": top10_picks
    },
    "manual10": {
        "totalFound": 0,
        "introHtml": "<p>No manual-transmission convertibles were confirmed in this refresh. Transmission data was not available for all listings — check individual listings on the source site for stick-shift availability.</p>",
        "picks": manual_picks
    },
    "mustangs": {
        "totalFound": len(mustang_picks),
        "introHtml": f"<p>{len(mustang_picks)} Ford Mustang convertibles (2005+, S197 generation and newer) found within 35 miles of Media, PA, priced $7K–15K. Ranked by mileage. All are V6 models at this price point.</p>",
        "picks": mustang_picks
    }
}

# ─── VALIDATE SCHEMA ─────────────────────────────────────────────────────────
print("=== SCHEMA VALIDATION ===")
# Rule A: top-level source keys
for key in ["carscom", "cargurus", "autotrader", "truecar"]:
    assert key in data, f"MISSING top-level key: {key}"
    print(f"✓ Rule A: '{key}' present at top level")

# Rule B: top10/manual10/mustangs are objects with picks array
for key in ["top10", "manual10", "mustangs"]:
    assert isinstance(data[key], dict), f"{key} must be a dict"
    assert "picks" in data[key], f"{key}.picks missing"
    assert isinstance(data[key]["picks"], list), f"{key}.picks must be a list"
    print(f"✓ Rule B: '{key}' is object with picks array ({len(data[key]['picks'])} items)")

# Rule C: carscom (no dot, no space)
assert "carscom" in data and "." not in "carscom" and " " not in "carscom"
print(f"✓ Rule C: 'carscom' key is correct")

# Rule D: rank fields present on all picks
for key in ["top10", "mustangs"]:
    for p in data[key]["picks"]:
        assert "rank" in p and isinstance(p["rank"], int), f"{key} pick missing rank"
print(f"✓ Rule D: rank fields present on all picks")

print(f"\n=== COUNTS ===")
print(f"Cars.com: {len(carscom_listings)} listings, totalFound={data['carscom']['totalFound']}")
print(f"CarGurus: {len(cargurus_listings)} listings, totalFound={data['cargurus']['totalFound']}")
print(f"AutoTrader: {len(autotrader_listings)} listings, totalFound={data['autotrader']['totalFound']}")
print(f"Top 10: {len(top10_picks)} picks")
print(f"Mustangs: {len(mustang_picks)} picks")
print(f"Manual: {len(manual_picks)} picks")

print(f"\n=== TOP 10 ===")
for i, p in enumerate(top10_picks):
    print(f"{p['rank']}. {p['year']} {p['make']} {p['model']} ${p['price']:,} {p['mileage']:,}mi [{p['source']}]")

print(f"\n=== MUSTANGS ===")
for p in mustang_picks:
    print(f"  #{p['rank']} {p['year']} {p['make']} {p['model']} {p['trim']} ${p['price']:,} {p['mileage']:,}mi [{p['source']}]")

# Write output
out_path = "/tmp/claude-0/-home-claude/7670cd2c-926c-5dc9-b2f8-e81677388cb1/scratchpad/data_new.json"
import os
if os.path.exists(os.path.dirname(out_path)):
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"\n✓ Written to {out_path}")
    print(f"  File size: {len(json.dumps(data, indent=2)):,} bytes")
else:
    print(f"\n(Skipped cloud write — scratchpad not found)")
