<html>
<head>
<!--
<section id="hackernews">
<h1>Articles I've liked on Hacker News</h1>
<div class="sidebar-block">
 <iframe marginheight="0" marginwidth="0"
     src="http://www.edparcell.com/misc/hn-saved.html"
     frameborder="0"
     style="border:0;height:525px;width:290px;">
  </iframe>
</div>
</section>
-->
<title>edparcell's Hacker News Saved Stories</title>
<style type="text/css"> 
body {
font-size: 62.5%;
text-align: left;
}
ul {
margin: 0px;
-webkit-padding-start: 40px;
display: block;
list-style-type: disc;
font-family: Arial, Helvetica, sans-serif;
background-color: transparent;
border-top-color: #999;
border-top-style: none;
border-top-width: 0px;
color: #999;
display: block;
float: none;
font-family: Arial, Helvetica, sans-serif;
padding: 0px;
}
li {
olor: #999;
list-style-type: none;
list-style-position: initial;
list-style-image: initial;
margin-top: 5px;
margin-right: 0px;
margin-bottom: 0px;
margin-left: 0px;
padding: 0px;
display: list-item;
}
li a {
color: #BC7134;
text-decoration: none;
margin: 0px;
padding: 0px;
cursor: auto;
font-size: 1.2em;
}
</style> 
</head>
<body>
<ul>
% for story in stories:
<li><a href="${story['link']}">${story['title']}</a></li>
% endfor
</ul>
</body>
</html>
