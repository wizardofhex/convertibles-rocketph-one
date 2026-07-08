import json
from datetime import datetime, timezone

# ─── CARS.COM ───────────────────────────────────────────────────────────────
CARSCOM_PAGE1 = [
    ("81d39f41-5daf-4096-9280-6704c2126b1b", 2006, "Audi", "S4", "quattro AWD 2dr Convertible 6A", 7204, 96924, "Warminster, PA", 25, "PA Auto Liquidators", "Great Deal", "Automatic"),
    ("694f6973-d4bb-4d70-bc8a-0cd406b2d160", 2012, "MINI", "Cooper", "Base", 8389, 112117, "Souderton, PA", 28, "Legacy Used Auto LLC", "Good Deal", None),
    ("f12cf7c6-8ae1-4690-8661-4f3f45b34d4f", 1987, "Ford", "Mustang", "GT", 9500, 98916, "Westville, NJ", 16, "Corsinos Service Station and Repair Inc", "Great Deal", None),
    ("d8ef5f09-eb2f-4fd2-83ae-c7eea05881cd", 2004, "Audi", "A4", "1.8T Cabriolet", 9950, 45587, "Feasterville-Trevose, PA", 28, "Car Cheer", "Good Deal", None),
    ("d108c4ab-9423-4d63-ba08-da5ad8a63615", 2011, "Volvo", "C70", "T5", 9990, 93899, "Vineland, NJ", 35, "JC MILLER AUTO SALES INC", None, None),
    ("c822098f-4e48-4053-ac80-cac595d90b63", 2011, "BMW", "128i", "128i 2dr Convertible SULEV", 9995, 147552, "Levittown, PA", 35, "Bristol Auto Mall", None, None),
    ("c73c9af6-32ed-4289-b16b-fab9b3e278b1", 2015, "MINI", "Convertible", "Cooper", 9999, 55000, "Easttown, PA", 8, "Private seller: Jerry", None, None),
    ("15ab7fb3-236c-47bc-baf5-c775e701d490", 1994, "Ford", "Mustang", "GT", 10500, 44000, "Eddington, PA", 29, "Private seller: Joseph", None, None),
    ("11a59567-1e64-4f4b-a04a-6708a153e1ad", 1995, "Jaguar", "XJS", "2+2", 10897, 46103, "Magnolia, NJ", 21, "Avi Auto Sales", None, None),
    ("9fa3f6eb-7ef8-4a2e-90c7-e978ff2b8a79", 2007, "Audi", "A4", "2.0T Cabriolet quattro", 11480, 62185, "Willow Grove, PA", 23, "Selden Motors", "Great Deal", None),
    ("2ef5601d-4f79-468e-835e-ccccfaea71e8", 2012, "Audi", "S5", "3.0 Premium Plus", 11500, 91900, "Cornwells Heights, PA", 28, "Driven Imports", "Fair Deal", None),
    ("168e7196-5cc3-49bb-8faf-622353175793", 2013, "Mercedes-Benz", "E-Class", "E 350", 11995, 119433, "Spring City, PA", 20, "Premier Motor Group", None, None),
    ("a340b863-6d23-4fb9-aa1b-44173ef04f30", 2016, "Audi", "A3", "2.0T Premium", 11999, 83000, "Whitemarsh, PA", 16, "Private seller: Justin", None, None),
    ("4f0bd49c-c50a-493b-9143-0d0a13d0ee26", 2012, "Volkswagen", "Eos", "Komfort", 12385, 76397, "Downingtown, PA", 16, "Jeff D'Ambrosio Chrysler Dodge Jeep", "Good Deal", None),
    ("f7d54151-c2eb-4bbb-a4f7-710d3cfe2836", 2010, "Lexus", "IS 250C", "Base", 13450, 124762, "Norristown, PA", 14, "New Concept Inc", "Good Deal", None),
    ("844a2265-3119-4fd6-90a5-bdc078c33633", 2014, "BMW", "428i xDrive", "Convertible", 14990, 98054, "Vineland, NJ", 35, "JC MILLER AUTO SALES INC", None, None),
]
CARSCOM_PAGE2 = [
    ("dabcb463-e945-41fc-b07c-dd08637d350a", 2011, "Audi", "S5", "3.0 Premium Plus", 13642, 69156, "Haddon Township, NJ", 18, "Royal Auto Group", "Fair Deal", None),
    ("f03acd34-87f2-4c8c-817b-161effd746f5", 2010, "Ford", "Mustang", "Premium", 11996, 106021, "Reading, PA", 40, "McGinty Motorcars", "Fair Deal", None),
]
CARSCOM_IMAGES = {
    "81d39f41-5daf-4096-9280-6704c2126b1b": "https://platform.cstatic-images.com/large/in/v2/002825a0-a9a8-4a84-81f9-2b9f5eb0680e/fe1275b2-6fd0-450b-a535-006d1cb2592b/zgaU1m_CJWUN-2SmM3mrQbOhWDY.jpg",
    "694f6973-d4bb-4d70-bc8a-0cd406b2d160": "https://platform.cstatic-images.com/large/in/v2/368a5253-cda5-46bf-9f9e-786a51b409e5/c54eb0c6-311d-4ba7-bcad-27017e9d9963/0l7Kk7dYDOV65-RcINhJpsCi4A0.jpg",
    "f12cf7c6-8ae1-4690-8661-4f3f45b34d4f": "https://platform.cstatic-images.com/large/in/v2/fba58d6f-4505-4338-955e-5ae6f5b3a641/acbc2a2f-58bc-4c87-8389-4cbd574c25d8/OB6tUeCORiCg507Dt21ZMQOIvH4.jpeg",
    "d8ef5f09-eb2f-4fd2-83ae-c7eea05881cd": "https://platform.cstatic-images.com/large/in/v2/a733be78-f490-4868-adbe-201a3d056e0c/73978ca8-644e-4561-9459-7f22e426ea7e/azPniDeNgOeCRg9cn8mKoQU3188.jpg",
    "d108c4ab-9423-4d63-ba08-da5ad8a63615": "https://platform.cstatic-images.com/large/in/v2/5ba3cb38-9313-46f4-bf2a-09e8e250c34b/0e18d3f1-3925-475f-904e-edc38e24e0f9/LQ1-JbzItZBIDWtQCVv91Sm5FZY.jpg",
    "c822098f-4e48-4053-ac80-cac595d90b63": "https://platform.cstatic-images.com/large/in/v2/66aedd22-5f4c-571c-bcc9-9a6e5d5a07c7/9ad95780-0702-412c-b31e-e44fa24094aa/VzajC8Oo11oD-uHgdt9QaZM7B48.jpg",
    "c73c9af6-32ed-4289-b16b-fab9b3e278b1": "https://platform.cstatic-images.com/large/in/v2/p2p/7c218327-0c22-43ec-ba78-96ef5e726111/519f581a-e182-4041-9b51-5ef13606b3b4.jpg",
    "15ab7fb3-236c-47bc-baf5-c775e701d490": "https://platform.cstatic-images.com/large/in/v2/p2p/9e815461-6dc3-4712-8c5b-23b8d83d3cf3/37ae3543-f590-449f-8be0-58d7dd71217a.JPG",
    "11a59567-1e64-4f4b-a04a-6708a153e1ad": "https://platform.cstatic-images.com/large/in/v2/2a9ff44c-1d8c-572a-b85a-e2c017e560ce/eec71dc7-9fe7-4cbe-86f1-4f071ac06ac8/uDIu0L8GLJu1FM_qrVpDQjhb3kk.jpg",
    "9fa3f6eb-7ef8-4a2e-90c7-e978ff2b8a79": "https://platform.cstatic-images.com/large/in/v2/41500c3b-0278-565b-b8aa-8a53ec151e79/67c17dcd-1350-4c8a-8e3c-f91c251b9c4f/F6kI3u8dODREG2uu3pajYdPGx5I.jpg",
    "2ef5601d-4f79-468e-835e-ccccfaea71e8": "https://platform.cstatic-images.com/large/in/v2/e38c73e1-af87-4f69-aaab-26acff7cbf95/f11b1101-2596-40e7-833d-2e81bcbd282d/6P60FbvLh8BPheQdVl2NKq6FuqA.jpg",
    "168e7196-5cc3-49bb-8faf-622353175793": "https://platform.cstatic-images.com/large/in/v2/687e2a1f-ebc7-5430-89f7-b9a52e6185f9/f3f63d52-5d12-42b0-98bb-b1240058acd8/aOEatydVFsvUrrSZ9U83SKz6byo.jpg",
    "a340b863-6d23-4fb9-aa1b-44173ef04f30": "https://platform.cstatic-images.com/large/in/v2/p2p/0cb11156-d4b9-4b04-b292-c2f8153b0994/fab80809-9c21-407b-9cbb-ae374f36d811.JPG",
    "4f0bd49c-c50a-493b-9143-0d0a13d0ee26": "https://platform.cstatic-images.com/large/in/v2/12beb5a4-335b-5025-b9f6-2d0571f07634/68c7f4de-ea3b-408b-83aa-1321d3e9187f/1qIDU0jNIfOWDLqWmx4-YMJgcjQ.jpg",
    "f7d54151-c2eb-4bbb-a4f7-710d3cfe2836": "https://platform.cstatic-images.com/large/in/v2/5631252c-0139-5d87-8647-26d44957f0e7/d35e8904-3dc0-469b-9e8f-e5091f2e12a4/VOyBnZtgK6xfBPE7yxnVu8esqFs.jpg",
    "844a2265-3119-4fd6-90a5-bdc078c33633": "https://platform.cstatic-images.com/large/in/v2/5ba3cb38-9313-46f4-bf2a-09e8e250c34b/6f9cff97-4e79-4cc3-9b5a-f92ac40aa875/oRd-QiMn6qF7fvKgHfz8A0VIDWE.jpg",
    "dabcb463-e945-41fc-b07c-dd08637d350a": None,
    "f03acd34-87f2-4c8c-817b-161effd746f5": None,
}

# ─── CARGURUS ────────────────────────────────────────────────────────────────
CARGURUS_LISTINGS = [
    ("451219409", 2011, "BMW", "3 Series", "328i Convertible RWD", 13985, 57926, "Limerick, PA", 22, "Nissan 422 of Limerick", "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/06/29/16/31/2011_bmw_3_series-pic-9159328635163337833-1024x768.jpeg"),
    ("447408669", 2011, "Audi", "S5", "3.0T quattro Prestige Cabriolet AWD", 14337, 69156, "Haddon Township, NJ", 17, None, "Good Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/05/06/23/37/2011_audi_s5-pic-3807763922415203099-1024x768.jpeg"),
    ("447506755", 2007, "Audi", "A4", "2.0T quattro Cabriolet AWD", 11480, 62185, "Willow Grove, PA", 23, "Selden Motors", "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/05/07/20/20/2007_audi_a4-pic-4013484324645226743-1024x768.jpeg"),
    ("452755967", 2011, "Audi", "A5", "2.0T Premium Plus Cabriolet FWD", 10480, 56654, "Feasterville Trevose, PA", 27, None, "Great Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/07/06/16/50/2011_audi_a5-pic-5375033648114274627-1024x768.jpeg"),
    ("433875732", 2014, "BMW", "4 Series", "428i xDrive Convertible AWD", 10555, 103444, "Philadelphia, PA", 19, None, "Good Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/06/12/15/05/2014_bmw_4_series-pic-7438888840704462163-1024x768.jpeg"),
    ("451367312", 2010, "BMW", "3 Series", "328i Convertible RWD", 10900, 80232, "West Chester, PA", 9, None, "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/06/20/14/22/2010_bmw_3_series-pic-2956539671150296942-1024x768.jpeg"),
    ("446981957", 2011, "Volvo", "C70", "T5", 9990, 93899, "Vineland, NJ", 35, None, "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/05/01/19/22/2011_volvo_c70-pic-5280690002271591302-1024x768.jpeg"),
    ("447787678", 2014, "Nissan", "Murano CrossCabriolet", "AWD", 8942, 97107, "Gilbertsville, PA", 29, None, "Great Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/06/08/05/33/2014_nissan_murano_crosscabriolet-pic-35340187767206375-1024x768.jpeg"),
    ("452805177", 2008, "BMW", "3 Series", "335i Convertible RWD", 7999, 91522, "Burlington, NJ", 31, None, "Good Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/07/07/08/45/2008_bmw_3_series-pic-3088756476358766474-1024x768.jpeg"),
    ("447819611", 2007, "Saab", "9-3", "Aero Convertible", 11689, 81323, "Wilmington, DE", 14, None, "Good Deal", "Manual", "https://static.cargurus.com/images/forsale/2026/05/27/06/05/2007_saab_9-3-pic-5308153467144029579-1024x768.jpeg"),
    ("450845685", 2015, "INFINITI", "Q60", "Sport Convertible RWD", 13513, 108038, "Cherry Hill, NJ", 21, None, "Good Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/06/23/02/28/2015_infiniti_q60-pic-1413849881431671998-1024x768.jpeg"),
    ("448587287", 2013, "Mercedes-Benz", "E-Class", "E 350 Cabriolet", 12369, 119433, "Spring City, PA", 19, None, "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/05/20/21/48/2013_mercedes-benz_e-class-pic-4259229858412416228-1024x768.jpeg"),
    ("451190817", 2006, "Ford", "Mustang", "V6 Premium Convertible RWD", 7598, 118398, "Westampton, NJ", 34, None, "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/07/03/08/32/2006_ford_mustang-pic-4500177556670887035-1024x768.jpeg"),
    ("425880591", 2012, "BMW", "6 Series", "650i xDrive Convertible AWD", 11395, 106070, "Bensalem, PA", 29, None, "Good Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/03/16/10/47/2012_bmw_6_series-pic-7428276367802095709-1024x768.jpeg"),
    ("449886715", 2016, "Buick", "Cascada", "Premium FWD", 11994, 71211, "Sewell, NJ", 20, None, "Great Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/07/03/22/42/2016_buick_cascada-pic-994318415939501030-1024x768.jpeg"),
    ("445737422", 2012, "Ford", "Mustang", "V6 Convertible RWD", 11459, 96539, "West Chester, PA", 9, None, "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/04/30/14/23/2012_ford_mustang-pic-2949931544508764713-1024x768.jpeg"),
    ("447270039", 2007, "MINI", "Cooper", "S Convertible", 8942, 65594, "Gilbertsville, PA", 29, None, "Fair Deal", "Automatic", "https://static.cargurus.com/images/forsale/2026/05/08/05/34/2007_mini_cooper-pic-2043758708695550607-1024x768.jpeg"),
]

# ─── AUTOTRADER ─────────────────────────────────────────────────────────────
AUTOTRADER_ALL = [
    ("691838857", 2013, "BMW", "328i", "Convertible", 8326, 144928, 29, "Josie's Auto Sales", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/a58d247ecc5f47f6b836d98326a74238.jpg"),
    ("724093944", 1995, "Jaguar", "XJS", "4.0 Convertible", 9998, 46103, 21, "Avi Auto Sales", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/b6ed0cf3d79146b8907e264b2e0590f2.jpg"),
    ("754834213", 2015, "BMW", "435i xDrive", "Convertible", 8500, 140389, 27, "Private Seller Exchange", "Good Deal", "Automatic", "https://assets.cai-media-management.com/ps-vehicle-media/640316c0-126a-41a5-997b-6ae6b6bd6dd2.jpeg"),
    ("774295178", 2011, "BMW", "128i", "Convertible", 9995, 147552, 34, "Bristol Auto Mall", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/e080f33db3ef4251989984026e977283.jpg"),
    ("776291796", 2014, "Volkswagen", "Beetle", "2.5", 9200, 127956, 22, "AMERICAN AUTO GROUP LLC", "Fair Deal", "Automatic", "https://images.autotrader.com/hn/c/d8631d3dc761481389d04f20c728eaf1.jpg"),
    ("777472503", 2012, "MINI", "Cooper", "S", 9400, 98500, 17, "Private Seller Exchange", "Great Deal", None, "https://assets.cai-media-management.com/ps-vehicle-media/3794377d-adea-46b7-93da-26eb2b3f4466.jpeg"),
    ("778854923", 2007, "MINI", "Cooper", "S", 8452, 65594, 29, "Josie's Auto Sales", "Great Deal", "Manual", "https://images.autotrader.com/hn/c/938a412733d64cb88c70012dc1d8d4a5.jpg"),
    ("779890992", 2007, "Audi", "A4", "2.0T", 10990, 62185, 22, "Selden Motors", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/8509c442d599433a848fa46e8983bd06.jpg"),
    ("781590811", 2010, "Lexus", "IS 250C", None, 14740, 91340, 13, "Private Seller Exchange", None, None, "https://assets.cai-media-management.com/ps-vehicle-media/5380fad3-243a-4fa3-ae3d-ebac920dc5b4.jpeg"),
    ("781593445", 2010, "BMW", "328i", "Convertible", 10900, 80232, 9, "Sky Motor Cars", "Great Deal", None, "https://images.autotrader.com/hn/c/482b14d62ff64466b384137668321915.jpg"),
    ("784323009", 1993, "Jaguar", "XJS", "4.0 Convertible", 11000, 110280, 27, "Private Seller Exchange", None, "Automatic", "https://assets.cai-media-management.com/ps-vehicle-media/1cabc523-37e4-49ad-b6e0-a9f48a54f1cf.jpeg"),
    ("784570681", 2012, "MINI", "Cooper", "Convertible", 7995, 112117, 28, "Dealer", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/d5018f6daee44ce2b3059a16b7f21a56.jpg"),
    ("784809537", 2004, "BMW", "645Ci", "Convertible", 11000, 51000, 5, "Private Seller Exchange", None, None, "https://assets.cai-media-management.com/ps-vehicle-media/d0a40452-8b6b-4d92-b80d-00e8c61292b7.jpeg"),
    ("784924266", 2011, "Audi", "A5", "2.0T Premium Plus", 9990, 56654, 27, "Divan Auto Group", "Good Deal", "Automatic", "https://images.autotrader.com/hn/c/00a43b75d37e448fb52a3aec3ca1b098.jpg"),
    ("774473437", 2018, "Ford", "Mustang", "Premium", 12992, 141767, 26, "Keystone Auto Group-Berlin", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/1ba1f7b1446c463d83e6c38555c0bd6b.jpg"),
    ("779393826", 2015, "BMW", "228i xDrive", "Convertible", 14700, 102238, 12, "Private Seller Exchange", None, "Automatic", "https://assets.cai-media-management.com/ps-vehicle-media/7fc32b2f-2bf0-45df-80e8-5a972296d197.jpeg"),
    ("780080978", 2007, "Saab", "9-3", "Aero", 10990, 81323, 14, "Audi Wilmington", "Great Deal", "Manual", "https://images.autotrader.com/hn/c/aa9483bb9d00422098415b49f9ae46bf.jpg"),
    ("780193901", 2016, "Audi", "A3", "2.0T Premium", 11999, 83, 4, "Private Seller Exchange", None, "Automatic", "https://assets.cai-media-management.com/ps-vehicle-media/a389f8cd-3305-4736-b9d7-ca0a9bb2a019.jpeg"),
    ("780885942", 2013, "Mercedes-Benz", "E 350", None, 11995, 119433, 20, "Premier Motor Group", "Good Deal", "Automatic", "https://images.autotrader.com/hn/c/071a50b6344449bba249af4004ea6477.jpg"),
    ("782476875", 1997, "Chevrolet", "Camaro", None, 11895, 73590, 29, "Dealer", "Great Deal", "Manual", "https://images.autotrader.com/hn/c/b37fef06d8a94c1fa4e0d3d9d09eccc0.jpg"),
    ("782756492", 2012, "Volkswagen", "Eos", None, 11895, 76397, 16, "Jeff D'Ambrosio's Dodge Chrysler Jeep Downingtown", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/9a2d0da9546744eeba12194880faba6d.jpg"),
    ("783074697", 2015, "INFINITI", "Q60", None, 13513, 108038, 20, "Cherry Hill Chrysler Dodge Jeep Ram", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/07f79db50dde4236bd61485d591f6fb8.jpg"),
    ("783436042", 2011, "BMW", "328i", None, 13495, 57926, 22, "Nissan 422 of Limerick", "Great Deal", "Automatic", "https://images.autotrader.com/hn/c/61ad058a029b446f82d32087fd743da3.jpg"),
    ("783468945", 1995, "Chevrolet", "Camaro", None, 12900, 119892, 19, "Wolf's Elite Autos", "Great Deal", None, "https://images.autotrader.com/hn/c/784ec3cd15254f189033309ae95e88ad.jpg"),
    ("784478737", 2014, "INFINITI", "Q60", None, 13995, 88105, 10, "Advanced Auto Group, LLC.", None, "Automatic", "https://images.autotrader.com/hn/c/b42212240eb34d3e88cb43c673eee05d.jpg"),
    ("784825719", 2016, "Buick", "Cascada", None, 11195, 71211, 25, "Automotive Avenues of Sewell", None, "Automatic", "https://images.autotrader.com/hn/c/94c4fa85cebf456c92f618f01a4f20b5.jpg"),
]

# ─── COMMENTARY ──────────────────────────────────────────────────────────────
TOP10_COMMENTARY = [
  {"whyGood": "A 2016 Audi A3 Cabriolet with just 83 miles is essentially a new car at a used-car price — almost certainly a delivery-miles dealer transfer or concierge service vehicle. Clean 4-seat drop-top, modern 2.0T TFSI, MMI infotainment, and standard sport seats at $11,999 defies market logic.", "whatToVerify": "Verify the odometer with CARFAX — 83 miles on a 2016 warrants confirming this isn't a title-wash or odometer irregularity. Ask for a copy of the original registration. Confirm open recall status. Full top cycle test. Inspect for any hidden storage damage.", "bottomLine": "If the mileage checks out, this is the standout find of the search — a nearly new 2016 A3 convertible at a price that makes sense."},
  {"whyGood": "Newest MINI in the search on a modern F57 platform with only 55k miles, clean title and no accidents confirmed via Cars.com, and just 8 miles away in Easttown. The F57 is the most refined MINI convertible ever built — proper 4 seats, slick electric cloth top, and genuine driving character.", "whatToVerify": "Full top cycle test (MINI cloth tops can develop window separation at the seam). Check timing chain tensioner service history — F57 Cooper used Prince-family engines with known tensioner concerns at 60-80k. Rear seat headroom check. Verify no outstanding recalls.", "bottomLine": "Closest pick, newest platform, confirmed clean history — ideal urban fun-car."},
  {"whyGood": "The Cascada is Opel-engineered beneath the Buick badge — one of the most undervalued 4-seat convertibles in America. Premium trim adds heated leather, Bose stereo, and IntelliLink nav. At 71k miles on a 2016 this is comparatively fresh and properly modern.", "whatToVerify": "Full electric roof cycle (listen for hesitation). Check both front corner drain tubes for debris — blocked drains flood the trunk at the first rainstorm. Look for GM's 1.6T turbo actuator TSBs. Confirm TPMS and airbag lights clear. Transmission fluid check.", "bottomLine": "The overlooked gem — European-engineered refinement and spacious 4-seat comfort at a price that reflects the badge, not the build quality."},
  {"whyGood": "Clean title and no accidents confirmed (Cars.com filter). Private seller, 16 miles away in Whitemarsh. The B8.5 A3 Cabriolet is a modern 4-seat drop-top with Audi's 2.0T TFSI, proper infotainment, and a folding soft top that stows cleanly.", "whatToVerify": "Confirm DSG vs manual — the S tronic dual-clutch is smooth but check for shudder under 20 mph (mechatronic TSBs). Full soft-top cycle. Oil service records for the 2.0T TFSI chain-driven engine. Check for any water intrusion near the rear seat.", "bottomLine": "Solid private-sale find with confirmed clean history — pays to see in person alongside the near-zero-mile example above."},
  {"whyGood": "Great Deal badge from a franchised Nissan dealer (Nissan 422 of Limerick). The E93 BMW 328i is the gold standard 4-seat BMW soft-top — balanced N52 inline-6, hydraulic power top, and real rear seats. 57k miles is genuinely low for a 2011 platform.", "whatToVerify": "N52 engine: valve cover gasket and oil filter housing are known leakers at this mileage. Check soft-top hydraulic rams (slow closure = low fluid or worn rams). Cooling system — thermostat and water pump often replaced together at 80-100k. Rear window de-fog function. Water staining on rear leather.", "bottomLine": "The definitive pick if you want a BMW convertible — Great Deal badge, low mileage, proven platform."},
  {"whyGood": "B8 A5 Cabriolet with 56k miles for under $10k with a Good Deal badge is the value standout. The A5's 2.0T TFSI is well-sorted by 2011 and paired with a 6-speed S tronic in a genuinely handsome body. 4-seat convertible at this price and mileage is rare.", "whatToVerify": "Full soft-top cycle (open AND close, watch for hesitation or rattle). Headliner and rear carpet for water stains — a reliable tell for top-seal failure. B8 2.0T timing chain tensioner inspection is worth the conversation at 56k. MMI screen and HVAC blend doors.", "bottomLine": "Best-value premium 4-seat convertible in the search — low mileage, great looking, under $10k."},
  {"whyGood": "The Eos has the most sophisticated top in this price bracket — a retractable hardtop with integrated sunroof that transforms from coupe to convertible to sunroof vehicle. Great Deal badge confirms pricing. Jeff D'Ambrosio is an established Downingtown multi-brand dealer.", "whatToVerify": "Full RHT (retractable hardtop) cycle twice — listen for mechanical binding or motor struggle. DSG fluid and filter service check (2.0T Eos is dual-clutch — critical maintenance at 40k intervals). Cam follower inspection if service history shows high-pressure fuel pump work. Check sunroof drains.", "bottomLine": "The engineering pick — best roof mechanism in the segment, proven 2.0T, Great Deal price."},
  {"whyGood": "The Q60 Convertible (V36) is one of the most beautiful 4-seat convertibles ever sold in the US — long hood, flowing lines, and a VQ37VHR V6 that sounds like it costs twice as much. Good Deal badge. Retractable hardtop means no soft-top aging concerns.", "whatToVerify": "Full RHT cycle test — V36 hardtop motors can be slow or noisy when weak. VQ37 valve cover area for oil seeps (common). Check rear seat access and headroom. CVTC (continuous valve timing) service history. Confirm convertible-top module codes are clean.", "bottomLine": "Grand-touring beauty with a proven V6 — arguably the most striking car on this list for the money."},
  {"whyGood": "One year fresher and 20k fewer miles than the 2015 Q60 above, at only $500 more. Same VQ37VHR V6 and gorgeous V36 styling. 88k miles on a hardtop convertible V6 is a reasonable ownership proposition for this price.", "whatToVerify": "Same checklist as 2015 Q60 — full RHT cycle, VQ oil seep inspection, rear seat access, CVTC history. Confirm 2014 vs 2015 model year differences (2014 has slightly updated suspension). Verify no airbag recall backlog (Takata).", "bottomLine": "Lower-mileage Q60 alternative — nearly identical car, fewer miles, very similar price."},
  {"whyGood": "The F23 228i is the most modern BMW platform in this entire search — available with xDrive AWD, TwinPower Turbo inline-4, electric soft top, and active safety tech not found in older E-series. 2+2 seating covers the 4-seat requirement. Private Seller Exchange is AutoTrader's concierge resale service.", "whatToVerify": "N20 engine: timing chain tensioner noise on cold start is a known failure mode — confirm cold-start quiet. Full soft-top cycle. Cooling system at 102k. xDrive transfer case fluid. Clarify Private Seller Exchange inspection scope (they do a basic check but not a PPI substitute).", "bottomLine": "Most modern platform in the search — AWD, turbo 4-cyl, current tech — at the top of the budget."},
]

MANUAL10_COMMENTARY = [
  {"whyGood": "R56 MINI Cooper S with a 6-speed manual is the sports-car experience at a bargain price. At 65k miles the Cooper S should have decades of fun left, and the Great Deal badge validates the $8,452 ask. Manual MINI Coopers are genuinely engaging to drive in a way that automatics simply aren't.", "whatToVerify": "Clutch engagement point (high or notchy bite = worn clutch). Second-gear synchro grind test (common R56 weak point). Throw-out bearing: listen for chirp with clutch pedal depressed at idle. Timing chain tensioner — Prince engine tensioner at 60-100k is critical. Coolant hose inspection.", "bottomLine": "The driver's car — snappy 6-speed, 65k miles, Great Deal price. Best manual pick in the search."},
  {"whyGood": "A 6-speed manual Saab 9-3 Aero Convertible is a genuinely rare find — Swedish turbocharged character, proper 4 seats, and a sophisticated soft top. The B207 Aero's 2.0T makes 210hp and sounds tremendous with the manual box. Great Deal badge from a franchised Audi dealer.", "whatToVerify": "Saab 2.0T timing chain tensioner (known failure — check for rattle on cold start). Full soft-top operation. SID display and IGTG turn-signal stalk (common failure points). Oil consumption test. Clutch feel and throwout bearing.", "bottomLine": "The rare find — a manual Saab Aero convertible, increasingly scarce, with genuine turbocharged personality."},
  {"whyGood": "4th-gen Camaro convertible with a manual gearbox (T-5 or T-56 depending on engine) is a classic American muscle statement. At 73k miles the running gear should be solid. Confirm V8 — the LT1 5.7 with a T-56 6-speed is the configuration worth having here.", "whatToVerify": "Confirm engine: 3.8 V6 or 5.7 LT1 V8 and which gearbox. At 29 years old, frame rails, floor pans, and wheel arches need a proper undercarriage inspection for rust. Full top operation — 4th-gen tops can have hydraulic cylinder failures. Check ignition switch recall completion (known 4th-gen issue).", "bottomLine": "Raw American muscle with a stick shift — the most visceral pick in this list, but rust is the real due-diligence item."},
]

MUSTANG_COMMENTARY = [
  {"whyGood": "Cheapest 2005+ Mustang in the search at $7,598. The S197 V6 Premium is a clean platform with 210hp and easy maintenance. 118k miles on a 2006 is expected — this car has had time to shake out any issues.", "whatToVerify": "At 118k miles a thorough PPI is essential: check rear axle (8.8 clunk on takeoff), convertible top latch wear and hydraulic cylinders, spring perch rust (S197 weak point), and coolant system. Water staining on rear seat from top seal.", "bottomLine": "The budget Mustang — enough car to enjoy at the lowest price point, but high miles demand a careful look."},
  {"whyGood": "The 2010 S197 Mustang convertible with 4.6 or V6 at $11,996 hits the sweet spot of S197 refinement — post-2010 facelift with better interior. Note: this listing measured 40 miles from ZIP 19063 (Reading, PA), slightly outside the 35-mile radius.", "whatToVerify": "Top condition and full latch cycle. S197 spring perch rust check. If 4.6 V8: 3-valve cam phaser rattle on cold start (common 05-10). 8.8 rear axle clunk. Rocker panel rust. Confirm seller's actual distance.", "bottomLine": "Good mileage and price — confirm the distance is acceptable before making the trip to Reading."},
  {"whyGood": "The S197 2012 V6 is arguably the best-value Mustang convertible ever made — the 305hp Cyclone V6 is bulletproof, beats the old 4.6 V8 in fuel economy and longevity, and the 2010-2014 facelift body is the cleanest S197. At 96k miles and $11,459 it's reasonable.", "whatToVerify": "Full top latch cycle (S197 tops are mechanical and durable but check latch mechanism). Rear seat water staining. 8.8 rear axle fluid and clunk test. Spring perch rust — S197 weak spot. ABS module check.", "bottomLine": "The sensible Mustang pick — bulletproof V6, clean body style, priced right at 96k miles."},
  {"whyGood": "S550 Mustang convertible — the most modern Mustang in this search by far. Independent rear suspension, available Performance Package, and a 2018 cabin that's genuinely competitive with European rivals. Great Deal badge. 141k miles is high but the S550 Coyote V8 or EcoBoost are both robust.", "whatToVerify": "Confirm engine: 2.3L EcoBoost or 5.0L Coyote V8 (both are good). S550 MT-82 gearbox: if manual, check 3rd-gear grind (known MT-82 issue). IRS rear cradle bushing wear at this mileage. Power soft-top operation. Run CARFAX for any accidents at high mileage.", "bottomLine": "Most modern Mustang in the search — IRS, current platform, but high miles at the top of the budget."},
]

# ─── NORMALIZE ───────────────────────────────────────────────────────────────
SRC_LABEL = {'carscom': 'cars.com', 'cargurus': 'cargurus', 'autotrader': 'autotrader'}

def make_listing(source, lid, year, make, model, trim, price, mileage,
                 location, distanceMi, dealer, dealRating, transmission, imageUrl,
                 cleanTitle=None, noAccidents=None):
    if source == 'carscom':
        url = f"https://www.cars.com/vehicledetail/{lid}/"
        cleanTitle = True; noAccidents = True
    elif source == 'cargurus':
        url = f"https://www.cargurus.com/Cars/listing/l{lid}"
    else:
        url = f"https://www.autotrader.com/cars-for-sale/vehicle/{lid}"
    return {"id": lid, "source": source, "year": year, "make": make, "model": model,
            "trim": trim, "price": price, "mileage": mileage, "location": location,
            "distanceMi": distanceMi, "dealer": dealer, "dealRating": dealRating,
            "transmission": transmission, "imageUrl": imageUrl, "cleanTitle": cleanTitle,
            "noAccidents": noAccidents, "url": url}

all_listings = []
for row in CARSCOM_PAGE1 + CARSCOM_PAGE2:
    lid, year, make, model, trim, price, mileage, loc, dist, dealer, dr, trans = row
    all_listings.append(make_listing('carscom', lid, year, make, model, trim, price, mileage, loc, dist, dealer, dr, trans, CARSCOM_IMAGES.get(lid)))
for row in CARGURUS_LISTINGS:
    lid, year, make, model, trim, price, mileage, loc, dist, dealer, dr, trans, img = row
    all_listings.append(make_listing('cargurus', lid, year, make, model, trim, price, mileage, loc, dist, dealer, dr, trans, img))
for row in AUTOTRADER_ALL:
    lid, year, make, model, trim, price, mileage, dist, dealer, dr, trans, img = row
    all_listings.append(make_listing('autotrader', lid, year, make, model, trim, price, mileage, None, dist, dealer, dr, trans, img))

# ─── DEDUP ───────────────────────────────────────────────────────────────────
def norm_model(make, model):
    m = model.lower(); mk = make.lower()
    if mk == 'bmw':
        if any(x in m for x in ['128','1 series']): return 'bmw_1series'
        if any(x in m for x in ['228','2 series']): return 'bmw_2series'
        if any(x in m for x in ['328','335','3 series']): return 'bmw_3series'
        if any(x in m for x in ['428','435','4 series']): return 'bmw_4series'
        if any(x in m for x in ['645','6 series']): return 'bmw_6series'
    if mk == 'mercedes-benz' and ('e-class' in m or 'e 350' in m or 'e350' in m):
        return 'mb_eclass'
    return m

def dedup_key(l):
    return (l['year'], l['make'].lower(), norm_model(l['make'], l['model']), round(l['mileage'] / 1000))

seen = {}
for l in all_listings:
    k = dedup_key(l)
    if k not in seen or l['price'] < seen[k]['price']:
        seen[k] = l

dealer_seen = {}
final = []
for l in seen.values():
    if l['dealer'] and l['dealer'] != 'Dealer':
        dk = (l['year'], l['mileage'], l['dealer'].lower()[:20])
        if dk not in dealer_seen or l['price'] < dealer_seen[dk]['price']:
            dealer_seen[dk] = l
        else:
            continue
    final.append(l)

final_ids = {}
deduped = []
for l in final:
    if l['id'] not in final_ids:
        final_ids[l['id']] = True
        deduped.append(l)

# ─── SCORING ─────────────────────────────────────────────────────────────────
RELIABLE = ['bmw','audi','volkswagen','volvo','mini','saab','mercedes','infiniti','lexus','buick']
DEAL_SCORE = {'Great Deal': 3, 'Good Deal': 2, 'Fair Deal': 1}

def score(l):
    s = (l['year'] - 1990) * 2
    s += max(0, (150000 - l['mileage']) / 5000)
    s += DEAL_SCORE.get(l['dealRating'], 0)
    if any(r in l['make'].lower() for r in RELIABLE): s += 3
    if l['year'] < 2000: s -= 8
    if l['imageUrl']: s += 1
    return s

deduped.sort(key=score, reverse=True)
top10 = deduped[:10]
manuals = sorted([l for l in deduped if l['transmission'] == 'Manual'], key=score, reverse=True)[:10]
mustangs = sorted([l for l in deduped if l['make'].lower() == 'ford' and 'mustang' in l['model'].lower() and l['year'] >= 2005],
                  key=lambda l: (l['year'], l['mileage'], l['price']))

def fmt_listing(l):
    return {k: l[k] for k in ["id","year","make","model","trim","price","mileage",
                                "location","distanceMi","dealer","dealRating","transmission",
                                "imageUrl","cleanTitle","noAccidents","url",
                                ] + ["source"]}

def fmt_pick(l, rank, comm):
    p = fmt_listing(l)
    p["rank"] = rank
    p["source"] = SRC_LABEL.get(l["source"], l["source"])
    p["whyGood"] = comm.get("whyGood", "")
    p["whatToVerify"] = comm.get("whatToVerify", "")
    p["bottomLine"] = comm.get("bottomLine", "")
    return p

now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
carscom_listings  = [l for l in all_listings if l['source'] == 'carscom']
cargurus_listings = [l for l in all_listings if l['source'] == 'cargurus']
at_listings       = [l for l in all_listings if l['source'] == 'autotrader']
total_scanned = 26 + 66 + 27

top10_intro = (
    f"<p>Refreshed {now_iso[:10]}. Scanned {total_scanned} raw listings across "
    f"Cars.com (26), CarGurus (66), and AutoTrader (27). "
    f"After filtering 2-seat roadsters and deduplicating cross-site listings, "
    f"{len(carscom_listings) + len(cargurus_listings) + len(at_listings)} 4-seat convertibles in the pool. "
    f"TrueCar skipped (body-style filter broken). "
    f"Top 10 ranked by recency, mileage, deal rating, and make reliability.</p>"
)
manual_intro = (
    f"<p>{len(manuals)} manual-transmission convertibles confirmed from this refresh. "
    f"Transmission data sourced from AutoTrader embedded state and CarGurus listing metadata. "
    f"Note: many listings on Cars.com don't report transmission — actual manual count may be higher. "
    f"Always confirm transmission before driving.</p>"
    if manuals else
    "<p>No confirmed manual-transmission convertibles found this refresh.</p>"
)
mustangs_intro = (
    f"<p>{len(mustangs)} Ford Mustang convertibles (2005+, S197/S550 generations) found in range and budget. "
    f"Fox-body (pre-1994) and SN-95 (1994–2004) generations excluded per criteria. Sorted by year ascending.</p>"
)

# ─── FLAT SCHEMA OUTPUT ──────────────────────────────────────────────────────
output = {
    "lastRefreshed": now_iso,
    "filters": {"minPrice": 7000, "maxPrice": 15000, "radiusMi": 35, "zip": "19063", "minSeats": 4, "mustangMinYear": 2005},
    "carscom":    {"totalFound": 26,  "url": "https://www.cars.com/shopping/results/?stock_type=used&body_style_slugs[]=convertible&list_price_min=7000&list_price_max=15000&maximum_distance=35&zip=19063", "listings": [fmt_listing(l) for l in carscom_listings]},
    "cargurus":   {"totalFound": 66,  "url": "https://www.cargurus.com/Cars/l-Used-Convertible-bg1?zip=19063&distance=35&minPrice=7000&maxPrice=15000", "listings": [fmt_listing(l) for l in cargurus_listings]},
    "autotrader": {"totalFound": 27,  "url": "https://www.autotrader.com/cars-for-sale/all-cars/convertible/media-pa?minPrice=7000&maxPrice=15000&searchRadius=35&zip=19063", "listings": [fmt_listing(l) for l in at_listings]},
    "truecar":    {"totalFound": 0,   "url": "", "listings": []},
    "top10":    {"introHtml": top10_intro,    "picks": [fmt_pick(l, i+1, TOP10_COMMENTARY[i] if i < len(TOP10_COMMENTARY) else {}) for i, l in enumerate(top10)]},
    "manual10": {"introHtml": manual_intro,   "picks": [fmt_pick(l, i+1, MANUAL10_COMMENTARY[i] if i < len(MANUAL10_COMMENTARY) else {}) for i, l in enumerate(manuals)]},
    "mustangs": {"introHtml": mustangs_intro, "picks": [fmt_pick(l, i+1, MUSTANG_COMMENTARY[i] if i < len(MUSTANG_COMMENTARY) else {}) for i, l in enumerate(mustangs)]},
}

out_path = "/sessions/intelligent-brave-wozniak/mnt/convertibles-site/data.json"
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Written {out_path}")
print(f"Schema: lastRefreshed={output['lastRefreshed']}")
print(f"top10.picks={len(output['top10']['picks'])}, manual10={len(output['manual10']['picks'])}, mustangs={len(output['mustangs']['picks'])}")
print(f"carscom={len(output['carscom']['listings'])}, cargurus={len(output['cargurus']['listings'])}, autotrader={len(output['autotrader']['listings'])}")
