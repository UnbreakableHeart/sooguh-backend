config = \
{
    'DATA_PORTAL_URL': 'https://www.data.go.kr',
    'SEARCH_CONFIG': {
        'SEARCH_BASE_URL': 'https://www.data.go.kr/tcs/dss/selectDataSetList.do?',
        'SEARCH_PER_PAGE': 40,
        'SEARCH_LIST_SELECTOR': 'div.result-list > ul',
        'ITEM_LINK_SELECTOR': 'dt > a',
        'TITLE_SELECTOR': 'span.title',
        'PROVIDER_SELECTOR': 'div.info-data > p:nth-child(1) > span.data',
        'MODIFIED_DATE_SELECTOR': 'div.info-data > p:nth-child(2) > span.data',
        'SEARCH_KEYWORD': ['헌옷 수거함', '의류 수거함']
    },
    'WEB_STATUS':{
        "OK": 200
    },
    'DOWNLOAD_BUTTON_XPATH': '//*[@id="tab-layer-file"]/div[2]/div[2]/a'
}
