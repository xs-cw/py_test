import pytest
import requests
import logging
import pprint

logging.basicConfig(level=logging.INFO)
pp = pprint.PrettyPrinter(indent=4)

baseUrl = "http://localhost:1234/test"

"""
url version 的格式
    新添加 1
    修改   2
"""
htmlUrlBase = 'http://www.baidu.com/index?version='
htmlUrlNew = htmlUrlBase+'1'
htmlUrlModify = htmlUrlBase+'2'


@pytest.fixture(scope='function')
def setup_function(request):
    def teardown_function():
        print("teardown_function called.")
    request.addfinalizer(teardown_function)  # 此内嵌函数做teardown工作
    print('setup_function called.')


@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called.")
    request.addfinalizer(teardown_module)
    print('setup_module called.')


def edit_html(caster_id, resource_id, url):
    r"""edithtml 原始接口"""

    resp = requests.put(baseUrl+"/html/modify", json={
        "casterId": caster_id,
        "htmlResourceId": resource_id,
        "htmlUrl": url
    })
    assert resp.ok
    res = resp.json()
    if res['code'] != 200:
        logging.error(res)
    assert res['code'] == 200
    return res


def get_html(caster_id):
    r"""查询资源列表"""

    resp = requests.get(f'{baseUrl}/html?casterId={caster_id}')
    assert resp.ok
    res = resp.json()
    assert res['code'] == 200
    # 数据检查 TODO
    # pp.pprint(res)
    return res


def edit_html_add(caster_id, url):
    r""" 添加html资源 """

    return edit_html(caster_id, '', url)


def html_url_in(caster_id, html_resource_id, url):
    r""" 判断url是否在列表中 """

    res = get_html(caster_id)
    list = res['data']['HtmlResourceList']['HtmlResource']
    add_success = False
    for resource in list:
        if resource['htmlUrl'] == url and resource['htmlResourceId'] == html_resource_id:
            add_success = True
    return add_success


@pytest.mark.html
def test_edit_html_add(setup_function):
    logging.info('测试添加')
    casterId = ""
    htmlUrl = htmlUrlNew
    # 添加html资源
    res = edit_html_add(casterId, htmlUrl)
    resourceId = res['data']['htmlResourceId']

    # 判断是否添加成功
    assert html_url_in(casterId, resourceId, htmlUrl)
    logging.info('添加资源成功!')


@pytest.mark.html
def test_edit_html_exist(setup_function):
    logging.info('测试添加已存在的url')
    casterId = ""
    htmlUrl = ''

    # 获取已有链接
    res = get_html(casterId)
    list = res['data']['HtmlResourceList']['HtmlResource']
    urls = [x['htmlUrl'] for x in list]
    assert len(urls) > 0
    htmlUrl = urls[0]

    # 添加html资源
    res = edit_html_add(casterId, htmlUrl)
    logging.info(res)
    resourceId = res['data']['htmlResourceId']

    # 判断是否添加成功
    assert html_url_in(casterId, resourceId, htmlUrl)
    logging.info('添加资源成功!')

    # 修改html资源
    htmlUrl = htmlUrlModify
    edit_html(casterId, resourceId, htmlUrl)

    # 是否修改成功
    assert html_url_in(casterId, resourceId, htmlUrl)
    logging.info('修改资源成功!')


@pytest.mark.html
def test_edit_html_modify(setup_function):
    logging.info('修改url')
    casterId = ""
    htmlUrl = htmlUrlModify
    htmlResourceId = ''
    # 原先url
    res = get_html(casterId)
    list = res['data']['HtmlResourceList']['HtmlResource']
    before = [x for x in list if x['htmlResourceId'] == htmlResourceId]
    assert len(before) == 1
    if htmlUrl == before[0]['htmlUrl']:
        htmlUrl = htmlUrl[:-1]+'3'

    # 修改
    edit_html(casterId, htmlResourceId, htmlUrl)
    # 是否修改成功
    assert html_url_in(casterId, htmlResourceId, htmlUrl)


@pytest.mark.caster
def test_apply_html():
    r"""  
    """
    requests.post(baseUrl+'/caster/control/applyhtml', json={
        "casterId": "",
        "htmlUrl": "",
        "htmlResourceId": "",
        "sceneType": ""
    })
    pass

@pytest.mark.caster
def test_cancel_apply_html():
    r""" 测试取消html资源的应用"""
    pass

@pytest.mark.caster
def test_add_html_video():
    r""" 测试将html链接生成视频资源并添加到通道中 """
    # 生成streamid

    # 检查url是否存在
    requests.post(baseUrl)
    pass
