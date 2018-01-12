#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Justin
@license: Beyondsoft License 
@file: report.py
@time: 2017/8/9 11:24
"""
__author__ = "Justin.jiang"
__version__ = "1.0"
class Template():
    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
</head>
<body>
<script language="javascript" type="text/javascript"><!--
output_list = Array();

/* level - 0:Summary; 1:Failed; 2:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level < 1) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level > 1) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
    }
}


function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            document.getElementById('div_'+tid).style.display = 'none'
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

/***
*功能：隐藏和显示div
*参数divDisplay：html标签id
***/
function all(divDisplay)
{
    if(divDisplay=="divOne_count")
    {
    document.getElementById("divOne_count").style.display = "block";
    document.getElementById("divOne_success").style.display = "none";
    document.getElementById("divOne_failed").style.display = "none";
    document.getElementById("divOne_error").style.display = "none";
    }
    if(divDisplay=="divOne_failed")
    {
    document.getElementById("divOne_failed").style.display = "block";
    document.getElementById("divOne_count").style.display = "none";
    document.getElementById("divOne_success").style.display = "none";
    document.getElementById("divOne_error").style.display = "none";
    }
    
    if(divDisplay=="divOne_success")
    {
    document.getElementById("divOne_success").style.display = "block";
    document.getElementById("divOne_count").style.display = "none";
    document.getElementById("divOne_failed").style.display = "none";
    document.getElementById("divOne_error").style.display = "none";
    }
    if(divDisplay=="divOne_error")
    {
    document.getElementById("divOne_error").style.display = "block";
    document.getElementById("divOne_count").style.display = "none";
    document.getElementById("divOne_failed").style.display = "none";
    document.getElementById("divOne_success").style.display = "none";
    }
   
}

/* obsoleted by detail in <div>
function showOutput(id, name) {
    var w = window.open("", //url
                    name,
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\n");
    d.write("<a href='javascript:window.close()'>close</a>\n");
    d.write("</pre>\n");
    d.close();
}
*/
--></script>

%(heading)s
%(report)s
%(details)s
%(ending)s

</body>
</html>
"""
    STYLESHEET_TMPL = """
    <style type="text/css" media="screen">
    body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
    table       { font-size: 100%; }
    pre         { }

    /* -- heading ---------------------------------------------------------------------- */
    h1 {
    	font-size: 16pt;
    	color: gray;
    }
    .heading {
        margin-top: 0ex;
        margin-bottom: 1ex;
    }

    .heading .attribute {
        margin-top: 1ex;
        margin-bottom: 0;
    }

    .heading .description {
        margin-top: 4ex;
        margin-bottom: 6ex;
    }

    /* -- css div popup ------------------------------------------------------------------------ */
    a.popup_link {
    }

    a.popup_link:hover {
        color: red;
    }

    .popup_window {
        display: none;
        position: relative;
        left: 0px;
        top: 0px;
        /*border: solid #627173 1px; */
        padding: 10px;
        background-color: #E6E6D6;
        font-family: "Lucida Console", "Courier New", Courier, monospace;
        text-align: left;
        font-size: 8pt;
        /* width: 500px; */
    }

    }
    /* -- report ------------------------------------------------------------------------ */
    #show_detail_line {
        margin-top: 3ex;
        margin-bottom: 1ex;
    }
    #result_table {
        width: 70%;
        border-collapse: collapse;
        border: 1px solid #777;
    }
    #header_row {
        font-weight: bold;
        color: white;
        background-color: #777;
    }
    #result_table td {
        border: 1px solid #777;
        padding: 2px;
    }
    td{text-align:center;vertical-align:middle;}
    #total_row  { font-weight: bold; }
    .passClass  { background-color: #6c6; }
    .failClass  { background-color: #c60; }
    .errorClass { background-color: #c00; }
    .passCase   { color: #6c6; }
    .failCase   { color: #c60; font-weight: bold; }
    .errorCase  { color: #c00; font-weight: bold; }
    .hiddenRow  { display: none; }
    .testcase   { margin-left: 2em; }
    a:hover{background-color: red;color:color:#FF0000;}


    /* -- ending ---------------------------------------------------------------------- */
    #ending {
    }

    </style>
    """
    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
    <h1>%(title)s</h1>
    %(parameters)s
    <h2 class='description'>%(description)s</h2>
    </div>
    """  # variables: (title, parameters, description)
    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>"""

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
    """  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #

    REPORT_TMPL = """
    <table id='result_table'>
    <colgroup>
    <col align='left' />
    <col align='right' />
    <col align='right' />
    <col align='right' />
    <col align='right' />
    <col align='right' />
    </colgroup>
    <tr id='header_row'>
        <td style="height: 50px;">  AI Test Model</td>
        <td>Count</td>
        <td>Pass</td>
        <td>Fail</td>
        <td>Error</td>
        <td>Success Rate</td>
    </tr>
    <tr id='total_row'>
        <td style="height: 40px;">%(model)s</td>
        <td><a href="javascript:all('divOne_count')">%(count)s</a></td>
        <td><a href="javascript:all('divOne_success')">%(Pass)s</a></td>
        <td><a href="javascript:all('divOne_failed')">%(fail)s</a></td>
        <td><a href="javascript:all('divOne_error')">%(error)s</a></td>
        <td>%(SuccessRate)s</td>
    </tr>
    </table>
    """

    DETAILS_TMPL = """
    <div id="divOne_%(type)s" style="display:none; margin-top:15px;">
        <table id='result_table'>
                %(list)s
        </table>
    </div>
    """
    # <div style="float: left;margin-left: 18px;">test:123, 1231 </div>
    # <div style="float: left;margin-left: 18px;">test:123, 1231 </div>
    # <div style="float: left;margin-left: 18px;">test:123, 1231 </div>

    RESULT_TMPL = """
    <td style="height:480px; width:250px;">
        <div style="height:50px;width:240px;margin-left:10px;">
            <div>
            <img style="float: left;margin-left: 5px;margin-top: 5px;" src=%(imgPath)s height="38" width="42"  alt="上海鲜花港 - 郁金香" />
            </div>
             <div style="float: left;margin-left: 8px;width: 170px;height: 40px;word-wrap: break-word;text-align: left;color:%(color)s;">%(coordinate)s</div>       
        </div>
        <div style="height:430px;width:240px;margin-top:18px;padding: 5px;">
            <img src=%(fullImage)s height="420" width="240" />
        </div>
    </td>
    
    """

    # LOGIN_INFO = """
    # <div style="float: left;margin-left: 8px;width: 180px;height: 40px;word-wrap: break-word;">%(coordinate)s</div>
    # """

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""


import datetime
class HTMLTestRunner(Template):
    def __init__(self):

        self.startTime = datetime.datetime.now()

    def getReportAttributes(self, startTime,success_count,failure_count,error_count):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """

        self.stopTime = datetime.datetime.now()
        duration = str(self.stopTime - startTime)
        startTime = str(self.startTime)[:19]
        status = []
        if success_count: status.append('Pass %s' % success_count)
        if failure_count: status.append('Failure %s' % failure_count)
        if error_count:   status.append('Error %s' % error_count)
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            ('Start Time', startTime),
            ('Duration', duration),
            ('Status', status),
        ]


    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL


    def _generate_heading(self,report_attrs,title,description):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=name,
                value=value,
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=title,
            parameters=''.join(a_lines),
            description=description,
        )
        return heading

    def _generate_report(self,model,count,success,failed,error):
        report = self.REPORT_TMPL % dict(
            test_list=''.join('12'),
            model = model,
            count=str(count),
            Pass=str(success),
            fail=str(failed),
            error=str(error),
            SuccessRate = str((float(success)/count)*100) + "%",
        )
        return report


    def temp(self,type,data):
        ls = ""
        number = len(data)
        yu = number - ((number / 5) * 5)
        zheng = number / 5
        image = ""
        result = ""
        # info
        current_index = 0
        for i in range(zheng):
            ls += "<tr style='padding-top:15px;'>"
            for k in range(5):
                current_index = 5 * i + k
                if data[current_index][2] == '':
                    result = "failed.png"
                    fullImage = "is_not_login_ui/" + data[current_index][0] +".jpg"
                    color = "red"
                else:
                    result = "success.png"
                    fullImage = "is_login_ui/" + data[current_index][0] + "_result.jpg"
                    color = "green"
                info = data[current_index][1]
                ls += self.RESULT_TMPL %dict(
                    imgPath = result,
                    coordinate =info,
                    fullImage = fullImage,
                color = color
                )
            ls += "</tr>"
        ls += "<tr>"
        for k in range(yu):
            current_index = current_index + 1

            if data[current_index][2] == '':
                result = "failed.png"
                fullImage = "is_not_login_ui/" + data[current_index][0] + ".jpg"
                color = "red"
            else:
                result = "success.png"
                fullImage = "is_login_ui/" + data[current_index][0] + "_result.jpg"
                color = "green"

            info = data[current_index][1]

            ls += self.RESULT_TMPL %dict(
                    imgPath = result,
                    coordinate =info,
                fullImage=fullImage,
                color=color
                )

        for m in range(5-yu):
            ls+= "<td style='border-color: white;'></td>"
        ls += "</tr>"
        s = self.DETAILS_TMPL % dict(
            list=ls,type=type )

        # details = ""
        #
        # details += self.LOGIN_INFO % dict(
        #         coordinate="user: 10,100"
        # )
        #
        # s = s % dict(
        #     info=details
        # )

        return s

    def _generate_details(self,all_data,success_data,failure_data,error_data):
        count = self.temp(data=all_data,type="count")
        success = self.temp(data= success_data,type="success")
        failed = self.temp(data = failure_data,type="failed")
        error = self.temp(data = error_data,type="error")
        return count+ success + failed + error

    def _generate_ending(self):
        return self.ENDING_TMPL

    def generateReport(self,startTime,all_data,model,description,title="AI Report"):
        success_data = []
        failure_data = []
        error_data = []
        for data in all_data:
            if data[2] == '':
                failure_data.append(data)
            else:
                success_data.append(data)

        report_attrs = self.getReportAttributes(startTime=startTime,success_count=len(success_data),failure_count=len(failure_data),error_count=len(error_data))
        output = self.HTML_TMPL % dict(
            title = title,
            generator='HTMLTestRunner %s' % __version__,
            stylesheet = self._generate_stylesheet(),
            heading = self._generate_heading(report_attrs,title=model,description=description),
            report = self._generate_report(model,count= len(success_data) + len(failure_data) + len(error_data), success=len(success_data),failed=len(failure_data),error=len(error_data)),
            details = self._generate_details(all_data,success_data,failure_data,error_data),
            ending =self._generate_ending(),
        )
        #print output
        return output

# startTime = datetime.datetime.now()
#
# result = [['84', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.08603692054748535], ['74', 'account:190,446,766,602;password:190,604,478,760;button:488,1006,592,1067;action:done', '/var/lib/jenkins/test_result//is_login_ui/74.xml_result.png', 10.319388151168823], ['51', 'account:113,313,607,383;password:113,429,607,499;button:63,652,657,731;action:done', '/var/lib/jenkins/test_result//is_login_ui/51.xml_result.png', 5.027316093444824], ['18', 'account:60,548,660,624;password:60,648,660,724;button:60,858,660,934;action:done', '/var/lib/jenkins/test_result//is_login_ui/18.xml_result.png', 1.166438102722168], ['44', 'account:126,902,1314,1108;password:126,1108,1314,1314;button:126,1384,1314,1552;action:done', '/var/lib/jenkins/test_result//is_login_ui/44.xml_result.png', 2.1601879596710205], ['28', 'account:207,297,936,432;password:207,465,936,600;button:54,783,1026,918;action:done', '/var/lib/jenkins/test_result//is_login_ui/28.xml_result.png', 2.74580717086792], ['111', 'account:41,334,1039,440;password:41,479,1039,585;button:496,674,584,733;action:done', '/var/lib/jenkins/test_result//is_login_ui/111.xml_result.png', 1.4998979568481445], ['60', 'account:157,565,697,664;password:156,666,516,767;button:33,826,685,916;action:done', '/var/lib/jenkins/test_result//is_login_ui/60.xml_result.png', 1.9737498760223389], ['32', 'account:108,801,1020,951;password:113,952,930,1102;button:134,1340,946,1484;action:done', '/var/lib/jenkins/test_result//is_login_ui/32.xml_result.png', 2.0875799655914307], ['100', 'account:429,608,1035,681;password:429,760,1035,833;button:270,1069,990,1219;action:done', '/var/lib/jenkins/test_result//is_login_ui/100.xml_result.png', 4.384140968322754], ['94', 'account:190,443,766,599;password:190,601,766,757;button:488,1003,592,1064;action:done', '/var/lib/jenkins/test_result//is_login_ui/94.xml_result.png', 11.711648941040039], ['42', 'account:30,312,1050,468;password:30,558,1050,714;button:30,905,1050,1049;action:done', '/var/lib/jenkins/test_result//is_login_ui/42.xml_result.png', 3.402453899383545], ['40', 'account:112,468,688,558;password:112,562,688,652;button:324,836,396,887;action:done', '/var/lib/jenkins/test_result//is_login_ui/40.xml_result.png', 3.784374952316284], ['102', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 1.5019431114196777], ['10', 'account:153,750,1023,888;password:153,937,1023,1075;button:45,1196,1035,1334;action:done', '/var/lib/jenkins/test_result//is_login_ui/10.xml_result.png', 5.152653932571411], ['24', 'account:195,740,1400,916;password:188,957,989,1133;button:80,1254,1360,1430;action:done', '/var/lib/jenkins/test_result//is_login_ui/24.xml_result.png', 1.4584228992462158], ['68', 'account:158,792,1013,894;password:158,1020,1013,1122;button:490,1370,592,1438;action:done', '/var/lib/jenkins/test_result//is_login_ui/68.xml_result.png', 5.439271926879883], ['39', 'account:140,269,507,369;password:140,389,684,489;button:36,549,684,645;action:done', '/var/lib/jenkins/test_result//is_login_ui/39.xml_result.png', 2.452550172805786], ['8', 'account:186,750,861,818;password:186,906,861,974;button:44,1178,1036,1293;action:done', '/var/lib/jenkins/test_result//is_login_ui/8.xml_result.png', 3.1384541988372803], ['110', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 3.1941280364990234], ['104', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 4.013957977294922], ['92', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.5994338989257812], ['7', 'account:420,351,1400,421;password:420,531,1400,601;button:240,855,1200,1035;action:done', '/var/lib/jenkins/test_result//is_login_ui/7.xml_result.png', 9.055290937423706], ['58', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 3.3973469734191895], ['49', 'account:222,552,874,696;password:222,699,874,843;button:72,990,1008,1134;action:done', '/var/lib/jenkins/test_result//is_login_ui/49.xml_result.png', 3.6826159954071045], ['62', 'account:172,549,644,607;password:172,665,596,723;button:56,892,664,972;action:done', '/var/lib/jenkins/test_result//is_login_ui/62.xml_result.png', 3.5646491050720215], ['30', 'account:183,525,1035,651;password:183,678,1035,804;button:30,942,1050,1050;action:done', '/var/lib/jenkins/test_result//is_login_ui/30.xml_result.png', 26.166118144989014], ['86', 'account:93,525,933,630;password:93,682,933,799;button:78,1097,1002,1235;action:done', '/var/lib/jenkins/test_result//is_login_ui/86.xml_result.png', 1.4501819610595703], ['41', 'account:411,861,1035,1026;password:135,1027,900,1192;button:60,1268,1020,1403;action:done', '/var/lib/jenkins/test_result//is_login_ui/41.xml_result.png', 2.8760998249053955], ['67', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.029707908630371094], ['50', 'account:113,313,607,383;password:113,429,607,499;button:63,652,657,731;action:done', '/var/lib/jenkins/test_result//is_login_ui/50.xml_result.png', 4.487282991409302], ['101', 'account:78,603,933,710;password:78,812,933,919;button:66,1021,1014,1178;action:done', '/var/lib/jenkins/test_result//is_login_ui/101.xml_result.png', 8.24616289138794], ['57', 'account:109,616,1089,739;password:109,800,1089,937;button:91,1285,1349,1446;action:done', '/var/lib/jenkins/test_result//is_login_ui/57.xml_result.png', 1.5316178798675537], ['80', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.6656789779663086], ['99', 'account:30,360,1050,498;password:30,555,1050,693;button:195,936,885,1086;action:done', '/var/lib/jenkins/test_result//is_login_ui/99.xml_result.png', 4.104306936264038], ['82', 'account:150,219,720,322;button:40,487,680,571;action:done', '/var/lib/jenkins/test_result//is_login_ui/82.xml_result.png', 3.3181560039520264], ['78', 'account:0,295,1080,439;password:0,440,1080,584;button:45,645,1035,789;action:done', '/var/lib/jenkins/test_result//is_login_ui/78.xml_result.png', 1.3429369926452637], ['73', 'account:248,853,937,912;password:248,1038,1025,1097;button:55,1184,1025,1299;action:done', '/var/lib/jenkins/test_result//is_login_ui/73.xml_result.png', 2.4907898902893066], ['66', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.04839301109313965], ['65', 'account:0,590,1080,725;password:0,726,1080,861;button:24,919,1056,1045;action:done', '/var/lib/jenkins/test_result//is_login_ui/65.xml_result.png', 2.009895086288452], ['17', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 8.273760080337524], ['13', 'account:135,570,945,735;password:135,825,945,990;button:135,1175,945,1325;action:done', '/var/lib/jenkins/test_result//is_login_ui/13.xml_result.png', 3.360214948654175], ['43', 'account:96,743,942,880;password:96,917,877,982;button:96,1198,984,1342;action:done', '/var/lib/jenkins/test_result//is_login_ui/43.xml_result.png', 2.8302979469299316], ['103', 'account:324,264,1021,384;password:324,412,1021,523;button:36,612,1044,756;action:done', '/var/lib/jenkins/test_result//is_login_ui/103.xml_result.png', 0.632457971572876], ['45', 'account:60,336,1020,410;password:60,538,816,612;button:60,737,1020,872;action:done', '/var/lib/jenkins/test_result//is_login_ui/45.xml_result.png', 2.132575035095215], ['59', 'account:284,289,1065,380;password:284,423,1065,514;button:45,673,1035,790;action:done', '/var/lib/jenkins/test_result//is_login_ui/59.xml_result.png', 8.152812004089355], ['69', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.5268352031707764], ['35', 'account:105,621,930,771;button:105,1200,975,1320;action:done', '/var/lib/jenkins/test_result//is_login_ui/35.xml_result.png', 2.9885928630828857], ['11', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 9.357287168502808], ['56', 'account:195,769,1005,919;password:195,949,1005,1099;button:75,1195,1005,1315;action:done', '/var/lib/jenkins/test_result//is_login_ui/56.xml_result.png', 3.048274040222168], ['33', 'account:274,730,658,850;button:114,1162,966,1297;action:done', '/var/lib/jenkins/test_result//is_login_ui/33.xml_result.png', 3.5505001544952393], ['113', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.5300679206848145], ['31', 'account:40,184,680,267;password:40,268,680,351;button:20,421,530,488;action:done', '/var/lib/jenkins/test_result//is_login_ui/31.xml_result.png', 3.575345039367676], ['85', 'account:170,526,1009,598;button:71,884,1009,1016;action:done', '/var/lib/jenkins/test_result//is_login_ui/85.xml_result.png', 2.5584118366241455], ['52', 'account:432,352,1361,512;password:432,550,1361,698;button:48,816,1392,1008;action:done', '/var/lib/jenkins/test_result//is_login_ui/52.xml_result.png', 3.162121057510376], ['64', 'account:192,503,684,578;button:30,643,690,729;action:done', '/var/lib/jenkins/test_result//is_login_ui/64.xml_result.png', 2.2746999263763428], ['25', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.03344106674194336], ['21', 'account:370,472,1246,554;password:290,554,1246,635;button:290,697,1246,795;action:done', '/var/lib/jenkins/test_result//is_login_ui/21.xml_result.png', 0.9766039848327637], ['77', 'account:0,569,1440,744;password:0,745,1440,920;button:70,1009,1370,1167;action:done', '/var/lib/jenkins/test_result//is_login_ui/77.xml_result.png', 6.391214847564697], ['79', 'account:123,1227,1317,1328;button:105,1476,1335,1826;action:done', '/var/lib/jenkins/test_result//is_login_ui/79.xml_result.png', 0.8145408630371094], ['4', 'account:243,369,981,504;password:243,558,981,693;button:114,989,966,1139;action:done', '/var/lib/jenkins/test_result//is_login_ui/4.xml_result.png', 3.809556007385254], ['1', 'account:0,387,1080,567;password:0,570,1080,750;button:30,810,1050,960;action:done', '/var/lib/jenkins/test_result//is_login_ui/1.xml_result.png', 4.938808917999268], ['76', 'account:141,378,1029,498;password:135,567,1035,632;button:45,696,1035,840;action:done', '/var/lib/jenkins/test_result//is_login_ui/76.xml_result.png', 5.009587049484253], ['90', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 0.6321899890899658], ['87', 'account:135,1014,1020,1104;password:135,1164,945,1254;button:75,1435,1005,1555;action:done', '/var/lib/jenkins/test_result//is_login_ui/87.xml_result.png', 1.4367380142211914], ['53', 'account:236,412,1260,540;password:236,606,1380,734;button:60,848,1380,1040;action:done', '/var/lib/jenkins/test_result//is_login_ui/53.xml_result.png', 2.6625430583953857], ['106', 'account:52,624,1028,706;password:52,759,1028,841;button:52,893,1028,1014;action:done', '/var/lib/jenkins/test_result//is_login_ui/106.xml_result.png', 0.3266589641571045], ['36', 'account:174,410,990,560;password:174,560,915,710;button:90,847,990,991;action:done', '/var/lib/jenkins/test_result//is_login_ui/36.xml_result.png', 4.851201057434082], ['98', 'account:360,880,1264,1056;password:360,1104,984,1280;button:660,1508,780,1588;action:done', '/var/lib/jenkins/test_result//is_login_ui/98.xml_result.png', 2.1308720111846924], ['89', 'account:368,490,1387,682;password:368,717,1247,909;button:53,1014,1387,1183;action:done', '/var/lib/jenkins/test_result//is_login_ui/89.xml_result.png', 2.9490017890930176], ['108', 'account:269,222,932,371;password:269,368,932,514;button:41,599,1039,728;action:done', '/var/lib/jenkins/test_result//is_login_ui/108.xml_result.png', 18.681509017944336], ['75', 'account:190,446,766,602;password:190,604,766,760;button:488,1006,592,1067;action:done', '/var/lib/jenkins/test_result//is_login_ui/75.xml_result.png', 9.486914157867432], ['72', 'account:123,267,1056,417;password:123,417,1056,567;button:24,870,1056,990;action:done', '/var/lib/jenkins/test_result//is_login_ui/72.xml_result.png', 14.509637117385864], ['46', 'account:60,336,1020,410;password:60,538,816,612;button:60,737,1020,872;action:done', '/var/lib/jenkins/test_result//is_login_ui/46.xml_result.png', 1.87717604637146], ['112', 'account:213,582,1035,716;password:213,717,854,851;button:37,918,1036,1041;action:done', '/var/lib/jenkins/test_result//is_login_ui/112.xml_result.png', 4.7261481285095215], ['71', 'account:201,438,1080,618;password:201,619,1080,799;button:240,1009,840,1154;action:done', '/var/lib/jenkins/test_result//is_login_ui/71.xml_result.png', 10.403412103652954], ['23', 'account:117,231,720,331;password:117,331,720,431;button:30,540,690,640;action:done', '/var/lib/jenkins/test_result//is_login_ui/23.xml_result.png', 2.780381917953491], ['16', 'account:183,555,1044,699;password:183,699,1044,843;button:48,909,1032,1035;action:done', '/var/lib/jenkins/test_result//is_login_ui/16.xml_result.png', 0.554656982421875], ['70', '\xe4\xb8\x8d\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe7\x99\xbb\xe5\xbd\x95\xe7\x95\x8c\xe9\x9d\xa2', '', 2.8418049812316895], ['38', 'account:312,632,993,700;button:48,972,1032,1116;action:done', '/var/lib/jenkins/test_result//is_login_ui/38.xml_result.png', 2.6214239597320557], ['12', 'account:60,593,1020,706;password:60,738,1020,853;button:60,963,1020,1088;action:done', '/var/lib/jenkins/test_result//is_login_ui/12.xml_result.png', 2.637094020843506], ['115', 'account:314,556,897,609;password:314,687,897,740;button:182,874,897,1012;action:done', '/var/lib/jenkins/test_result//is_login_ui/115.xml_result.png', 4.599721908569336], ['55', 'account:90,539,990,707;password:90,707,990,875;button:90,1110,990,1254;action:done', '/var/lib/jenkins/test_result//is_login_ui/55.xml_result.png', 1.917733907699585], ['34', 'account:244,348,1400,520;password:244,540,1400,712;button:32,956,941,1136;action:done', '/var/lib/jenkins/test_result//is_login_ui/34.xml_result.png', 2.956636905670166], ['54', 'account:0,357,1440,533;password:0,534,1340,710;button:60,851,1380,1051;action:done', '/var/lib/jenkins/test_result//is_login_ui/54.xml_result.png', 3.608203887939453], ['15', 'account:324,261,1021,381;password:324,409,1021,520;button:36,609,1044,753;action:done', '/var/lib/jenkins/test_result//is_login_ui/15.xml_result.png', 0.6361510753631592], ['105', 'account:90,447,720,548;password:90,548,720,649;button:360,679,698,781;action:done', '/var/lib/jenkins/test_result//is_login_ui/105.xml_result.png', 2.822524070739746], ['14', 'account:0,265,1080,397;password:0,398,1005,530;button:45,636,1035,786;action:done', '/var/lib/jenkins/test_result//is_login_ui/14.xml_result.png', 3.6620049476623535], ['95', 'account:84,306,612,376;password:84,400,554,470;button:92,520,628,620;action:done', '/var/lib/jenkins/test_result//is_login_ui/95.xml_result.png', 3.972872018814087], ['47', 'account:183,950,1002,1058;password:189,1136,670,1244;button:81,1394,1002,1508;action:done', '/var/lib/jenkins/test_result//is_login_ui/47.xml_result.png', 4.639998912811279]]
# # success_count = 0
# # failed_count = 0
# # error_count = 0
# # for data in result:
# #     if data[2] == '':
# #         failed_count += 1
# #     else:
# #         success_count += 1
# # print failed_count,success_count,error_count
# open("index.html","w").write(HTMLTestRunner().generateReport(startTime=startTime,all_data=result,model="AutoLogin",description="自动登录"))