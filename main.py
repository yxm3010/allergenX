import qrcode

def make_qrcode(cust, url):
    img = qrcode.make(url)
    fname = cust + '.png'
    img.save(fname)

make_qrcode('mcdonalds','https://corporate.mcdonalds.com/corpmcd/home.html')

