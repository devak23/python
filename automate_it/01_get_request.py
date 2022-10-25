import requests

r = requests.get("http://www.google.com")
print("Response Object: ", r)
print("Response text: ", r.text)

# running the program produces the following:
# Response Object:  <Response [200]>
# Response text:  <!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en-IN"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title><script>(function(){window.google={kEI:'nShcWqjHE8ep0gSWtJDwAg',kEXPI:'1352552,1354277,1354916,1355219,1355458,1355528,1355675,1355761,1355793,1356039,1356341,1356947,1357038,1357219,1357320,1357393,1357394,3700259,3700521,4029815,4031109,4040137,4043492,4045841,4048347,4081039,4081165,4095910,4097153,4097194,4097469,4097922,4097929,4098733,4098740,4098752,4101430,4101437,4102238,4103209,4103475,4109316,4109489,4112771,4114597,4115697,4116350,4116724,4116731,4116926,4116928,4116935,4117980,4118798,4119032,4119034,4119036,4120660,4121174,4122511,4123641,4123830,4123850,4124091,4124850,4125837,4126204,4126754,4127262,4127418,4127473,4127744,4127863,4128586,4128624,4129001,4129520,4129633,4130775,4131247,4131834,4131853,4133114,4135025,4135249,4135926,4135934,4136073,4136092,4136137,4137595,4137646,4138238,4140032,4140733,4141241,4141339,4141445,4141469,4141706,4141916,4142071,4142328,4142420,4142503,4142633,4142829,4142834,4142847,4143278,4143527,4143677,4143833,4143854,4143901,4144324,4144442,4144704,4145088,4145461,4145485,4145772,4145836,4146146,4146192,4146880,4146998,4147026,4147097,4147443,4147487,4147951,4147977,4148268,4148304,4148643,4148871,4149139,6512307,10200083,10200095,10202524,10202562,15807764,19000288,19000423,19000427,19001999,19002287,19002288,19002366,19002548,19002880,19003321,19003323,19003325,19003326,19003328,19003329,19003330,19003407,19003408,19003409,19004309,19004516,19004517,19004518,19004519,19004520,19004521,19004664,19004668,19004670,19004692,19004712,19004721,41317155',authuser:0,kscs:'c9c918f0_nShcWqjHE8ep0gSWtJDwAg',u:'c9c918f0',kGL:'IN'};google.kHL='en-IN';})();(function(){google.lc=[];google.li=0;google.getEI=function(a){for(var b;a&&(!a.getAttribute||!(b=a.getAttribute("eid")));)a=a.parentNode;return b||google.kEI};google.getLEI=function(a){for(var b=null;a&&(!a.getAttribute||!(b=a.getAttribute("leid")));)a=a.parentNode;return b};google.https=function(){return"https:"==window.location.protocol};google.ml=function(){return null};google.wl=function(a,b){try{google.ml(Error(a),!1,b)}catch(d){}};google.time=function(){return(new Date).getTime()};google.log=function(a,b,d,c,g){if(a=google.logUrl(a,b,d,c,g)){b=new Image;var e=google.lc,f=google.li;e[f]=b;b.onerror=b.onload=b.onabort=function(){delete e[f]};google.vel&&google.vel.lu&&google.vel.lu(a);b.src=a;google.li=f+1}};google.logUrl=function(a,b,d,c,g){var e="",f=google.ls||"";d||-1!=b.search("&ei=")||(e="&ei="+google.getEI(c),-1==b.search("&lei=")&&(c=google.getLEI(c))&&(e+="&lei="+c));c="";!d&&google.cshid&&-1==b.search("&cshid=")&&(c="&cshid="+google.cshid);a=d||"/"+(g||"gen_204")+"?atyp=i&ct="+a+"&cad="+b+e+f+"&zx="+google.time()+c;/^http:/i.test(a)&&google.https()&&(google.ml(Error("a"),!1,{src:a,glmm:1}),a="");return a};}).call(this);(function(){google.y={};google.x=function(a,b){if(a)var c=a.id;else{do c=Math.random();while(google.y[c])}google.y[c]=[a,b];return!1};google.lm=[];google.plm=function(a){google.lm.push.apply(google.lm,a)};google.lq=[];google.load=function(a,b,c){google.lq.push([[a],b,c])};google.loadAll=function(a,b){google.lq.push([a,b])};}).call(this);google.f={};var a=window.location,b=a.href.indexOf("#");if(0<=b){var c=a.href.substring(b+1);/(^|&)q=/.test(c)&&-1==c.indexOf("#")&&a.replace("/search?"+c.replace(/(^|&)fp=[^&]*/g,"")+"&cad=h")};</script><style>#gbar,#guser{font-size:13px;padding-top:1px !important;}#gbar{height:22px}#guser{padding-bottom:7px !important;text-align:right}.gbh,.gbd{border-top:1px solid #c9d7f1;font-size:1px}.gbh{height:0;position:absolute;top:24px;width:100%}@media all{.gb1{height:22px;margin-right:.5em;vertical-align:top}#gbar{float:left}}a.gb1,a.gb4{text-decoration:underline !important}a.gb1,a.gb4{color:#00c !important}.gbi .gb4{color:#dd8e27 !important}.gbf .gb4{color:#900 !important}
# </style><style>body,td,a,p,.h{font-family:arial,sans-serif}body{margin:0;overflow-y:scroll}#gog{padding:3px 8px 0}td{line-height:.8em}.gac_m td{line-height:17px}form{margin-bottom:20px}.h{color:#36c}.q{color:#00c}.ts td{padding:0}.ts{border-collapse:collapse}em{font-weight:bold;font-style:normal}.lst{height:25px;width:496px}.gsfi,.lst{font:18px arial,sans-serif}.gsfs{font:17px arial,sans-serif}.ds{display:inline-box;display:inline-block;margin:3px 0 4px;margin-left:4px}input{font-family:inherit}a.gb1,a.gb2,a.gb3,a.gb4{color:#11c !important}body{background:#fff;color:black}a{color:#11c;text-decoration:none}a:hover,a:active{text-decoration:underline}.fl a{color:#36c}a:visited{color:#551a8b}a.gb1,a.gb4{text-decoration:underline}a.gb3:hover{text-decoration:none}#ghead a.gb2:hover{color:#fff !important}.sblc{padding-top:5px}.sblc a{display:block;margin:2px 0;margin-left:13px;font-size:11px}.lsbb{background:#eee;border:solid 1px;border-color:#ccc #999 #999 #ccc;height:30px}.lsbb{display:block}.ftl,#fll a{display:inline-block;margin:0 12px}.lsb{background:url(/images/nav_logo229.png) 0 -261px repeat-x;border:none;color:#000;cursor:pointer;height:30px;margin:0;outline:0;font:15px arial,sans-serif;vertical-align:top}.lsb:active{background:#ccc}.lst:focus{outline:none}</style><script></script><link href="/images/branding/product/ico/googleg_lodp.ico" rel="shortcut icon"></head><body bgcolor="#fff"><script>(function(){var src='/images/nav_logo229.png';var iesg=false;document.body.onload = function(){window.n && window.n();if (document.images){new Image().src=src;}
# if (!iesg){document.f&&document.f.q.focus();document.gbqf&&document.gbqf.q.focus();}
# }
# })();</script><div id="mngb"> <div id=gbar><nobr><b class=gb1>Search</b> <a class=gb1 href="http://www.google.co.in/imghp?hl=en&tab=wi">Images</a> <a class=gb1 href="http://maps.google.co.in/maps?hl=en&tab=wl">Maps</a> <a class=gb1 href="https://play.google.com/?hl=en&tab=w8">Play</a> <a class=gb1 href="http://www.youtube.com/?gl=IN&tab=w1">YouTube</a> <a class=gb1 href="http://news.google.co.in/nwshp?hl=en&tab=wn">News</a> <a class=gb1 href="https://mail.google.com/mail/?tab=wm">Gmail</a> <a class=gb1 href="https://drive.google.com/?tab=wo">Drive</a> <a class=gb1 style="text-decoration:none" href="https://www.google.co.in/intl/en/options/"><u>More</u> &raquo;</a></nobr></div><div id=guser width=100%><nobr><span id=gbn class=gbi></span><span id=gbf class=gbf></span><span id=gbe></span><a href="http://www.google.co.in/history/optout?hl=en" class=gb4>Web History</a> | <a  href="/preferences?hl=en" class=gb4>Settings</a> | <a target=_top id=gb_70 href="https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=http://www.google.co.in/%3Fgfe_rd%3Dcr%26dcr%3D0%26ei%3DnShcWqSICLCdX9KtkKAN" class=gb4>Sign in</a></nobr></div><div class=gbh style=left:0></div><div class=gbh style=right:0></div> </div><center><br clear="all" id="lgpd"><div id="lga"><div style="padding:28px 0 3px"><div style="height:110px;width:276px;background:url(/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png) no-repeat" title="Google" align="left" id="hplogo" onload="window.lol&&lol()"><div style="color:#777;font-size:16px;font-weight:bold;position:relative;top:70px;left:218px" nowrap="">India</div></div></div><br></div><form action="/search" name="f"><table cellpadding="0" cellspacing="0"><tr valign="top"><td width="25%">&nbsp;</td><td align="center" nowrap=""><input name="ie" value="ISO-8859-1" type="hidden"><input value="en-IN" name="hl" type="hidden"><input name="source" type="hidden" value="hp"><input name="biw" type="hidden"><input name="bih" type="hidden"><div class="ds" style="height:32px;margin:4px 0"><input style="color:#000;margin:0;padding:5px 8px 0 6px;vertical-align:top" autocomplete="off" class="lst" value="" title="Google Search" maxlength="2048" name="q" size="57"></div><br style="line-height:0"><span class="ds"><span class="lsbb"><input class="lsb" value="Google Search" name="btnG" type="submit"></span></span><span class="ds"><span class="lsbb"><input class="lsb" value="I'm Feeling Lucky" name="btnI" onclick="if(this.form.q.value)this.checked=1; else top.location='/doodles/'" type="submit"></span></span></td><td class="fl sblc" align="left" nowrap="" width="25%"><a href="/advanced_search?hl=en-IN&amp;authuser=0">Advanced search</a><a href="/language_tools?hl=en-IN&amp;authuser=0">Language tools</a></td></tr></table><input id="gbv" name="gbv" type="hidden" value="1"></form><div id="gac_scont"></div><div style="font-size:83%;min-height:3.5em"><br><div id="als"><style>#als{font-size:small;margin-bottom:24px}#_eEe{display:inline-block;line-height:28px;}#_eEe a{padding:0 3px;}._lEe{display:inline-block;margin:0 2px;white-space:nowrap}._PEe{display:inline-block;margin:0 2px}</style><div id="_eEe">Google offered in: <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=hi&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAU">&#2361;&#2367;&#2344;&#2381;&#2342;&#2368;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=bn&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAY">&#2476;&#2494;&#2434;&#2482;&#2494;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=te&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAc">&#3108;&#3142;&#3122;&#3137;&#3095;&#3137;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=mr&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAg">&#2350;&#2352;&#2366;&#2336;&#2368;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=ta&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAk">&#2980;&#2990;&#3007;&#2996;&#3021;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=gu&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAo">&#2711;&#2753;&#2716;&#2736;&#2750;&#2724;&#2752;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=kn&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAs">&#3221;&#3240;&#3277;&#3240;&#3233;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=ml&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCAw">&#3374;&#3378;&#3375;&#3390;&#3379;&#3330;</a>  <a href="http://www.google.co.in/setprefs?sig=0_91-oGWfoxtSaqCci7072vcMYAWY%3D&amp;hl=pa&amp;source=homepage&amp;sa=X&amp;ved=0ahUKEwjoierVi9nYAhXHlJQKHRYaBC4Q2ZgBCA0">&#2602;&#2672;&#2588;&#2622;&#2604;&#2624;</a> </div></div></div><span id="footer"><div style="font-size:10pt"><div style="margin:19px auto;text-align:center" id="fll"><a href="/intl/en/ads/">Advertising Programs</a><a href="http://www.google.co.in/services/">Business Solutions</a><a href="https://plus.google.com/104205742743787718296" rel="publisher">+Google</a><a href="/intl/en/about.html">About Google</a><a href="http://www.google.co.in/setprefdomain?prefdom=US&amp;sig=__yS9W42JkvqOcrGeSHQf_nPA9r50%3D" id="fehl">Google.com</a></div></div><p style="color:#767676;font-size:8pt">&copy; 2018 - <a href="/intl/en/policies/privacy/">Privacy</a> - <a href="/intl/en/policies/terms/">Terms</a></p></span></center><script>(function(){window.google.cdo={height:0,width:0};(function(){var a=window.innerWidth,b=window.innerHeight;if(!a||!b){var c=window.document,d="CSS1Compat"==c.compatMode?c.documentElement:c.body;a=d.clientWidth;b=d.clientHeight}a&&b&&(a!=google.cdo.width||b!=google.cdo.height)&&google.log("","","/client_204?&atyp=i&biw="+a+"&bih="+b+"&ei="+google.kEI);}).call(this);})();</script><div id="xjsd"></div><div id="xjsi"><script>(function(){function c(b){window.setTimeout(function(){var a=document.createElement("script");a.src=b;google.timers&&google.timers.load.t&&google.tick("load",{gen204:"xjsls",clearcut:31});document.getElementById("xjsd").appendChild(a)},0)}google.dljp=function(b,a){google.xjsu=b;c(a)};google.dlj=c;}).call(this);(function(){var r=[];google.plm(r);})();if(!google.xjs){window._=window._||{};window._DumpException=window._._DumpException=function(e){throw e};google.dljp('/xjs/_/js/k\x3dxjs.hp.en_US.z-wHmCpdpCg.O/m\x3dsb_he,d/am\x3dABA/rt\x3dj/d\x3d1/t\x3dzcms/rs\x3dACT90oFx1X67u0OoYMJC5LxWb3mLZHZm_Q','/xjs/_/js/k\x3dxjs.hp.en_US.z-wHmCpdpCg.O/m\x3dsb_he,d/am\x3dABA/rt\x3dj/d\x3d1/t\x3dzcms/rs\x3dACT90oFx1X67u0OoYMJC5LxWb3mLZHZm_Q');google.xjs=1;}google.pmc={"sb_he":{"agen":true,"cgen":true,"client":"heirloom-hp","dh":true,"dhqt":true,"ds":"","ffql":"en","fl":true,"host":"google.co.in","isbh":28,"jam":0,"jsonp":true,"msgs":{"cibl":"Clear Search","dym":"Did you mean:","lcky":"I\u0026#39;m Feeling Lucky","lml":"Learn more","oskt":"Input tools","psrc":"This search was removed from your \u003Ca href=\"/history\"\u003EWeb History\u003C/a\u003E","psrl":"Remove","sbit":"Search by image","srch":"Google Search"},"nds":true,"ovr":{},"pq":"","refpd":true,"rfs":[],"sbpl":24,"sbpr":24,"scd":10,"sce":5,"stok":"GVhsvRopDPLNNE1P8TAwombFAe0"},"d":{},"YFCs/g":{}};google.x(null,function(){});(function(){var ctx=[]
# ;google.jsc && google.jsc.x(ctx);})();</script></div></body></html>

payload = {'q': 'devak23'}
r = requests.get('https://github.com/search', params=payload)
print("Request URL: ", r.url)

# this produces
# Request URL:  https://github.com/search?q=devak23

payload = {'key1': 'value1'}
response = requests.post("http://httpbin.org/post", data=payload)
print(response.text)

# running the above produces the following:
# {
#   "args": {},
#   "data": "",
#   "files": {},
#   "form": {
#     "key1": "value1"
#   },
#   "headers": {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Cache-Control": "max-age=0",
#     "Connection": "close",
#     "Content-Length": "11",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Host": "httpbin.org",
#     "User-Agent": "python-requests/2.18.4"
#   },
#   "json": null,
#   "origin": "124.155.241.206",
#   "url": "http://httpbin.org/post"
# }
