import pandas as pd
import requests
import json


def get_stat_from_url():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    cn_area = requests.get(url).json()
    cn_data = json.loads(cn_area['data'])
    update_time = cn_data['lastUpdateTime']
    all_countires = cn_data['areaTree']
    for country_data in all_countires:
        if not country_data['name'] == '中国':
            continue
        else:
            all_region_result_list = []
            all_regions = country_data['children']
            for region_data in all_regions:
                province_name = region_data['name']
                all_cities = region_data['children']
                for city_data in all_cities:
                    city_name = city_data['name']
                    city_total = city_data['total']
                    region_result = {'province': province_name, 'city': city_name}
                    region_result.update(city_total)
                    region_result.update({'update_time': update_time})
                    all_region_result_list.append(region_result)

    all_region_df = pd.DataFrame(all_region_result_list)
    print(all_region_df.to_string())
    all_region_df.to_excel('all_region_data.xlsx', index=False)


if __name__ == '__main__':
    get_stat_from_url()