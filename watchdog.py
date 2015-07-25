import easygui
a = 5
cardid = "1"
orderid = 1
seller = "1"
easygui.msgbox(msg="尊敬的卖家(卡号%s)，请放入您订单号为%d(卖家姓名为%s)的商品！"%(cardid,orderid,seller),title="中转箱")