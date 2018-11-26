# encoding=utf-8

from wechatpy import WeChatClient

import setting

if __name__ == '__main__':

    client = WeChatClient(setting.WechatConf['appid'], setting.WechatConf['secret'])
    menu_data = {
        "button":[
            {
                "type":"click",
                "name":"点击",
                "key":"BTN_A"
            },
            {
                "name":"菜单",
                "sub_button":[
                    {
                        "type":"view",
                        "name":"跳转",
                        "url":"http://scumer.com/"
                    },
                    {
                        "type":"click",
                        "name":"点击",
                        "key":"BTN_B"
                    }
                ]
            }
        ]
    }
    client.menu.create(menu_data)


