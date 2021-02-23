/*!

=========================================================
* Black Dashboard React - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/black-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/black-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
/*! For license information please see main.5634ebef.chunk.js.LICENSE.txt */
(this["webpackJsonpdual-mag-dashboard-react"]=this["webpackJsonpdual-mag-dashboard-react"]||[]).push([[0],{55:function(e,a,t){},56:function(e,a,t){},57:function(e,a,t){},58:function(e,a,t){},60:function(e,a,t){"use strict";t.r(a);var n=t(2),s=t(13),i=t(1),r=t.n(i),c=t(16),o=t.n(c),l=t(17),m=t(9),g=t(10),d=t(18),b=t(5),u=t.n(b),j=t(62),h=t(63),p=t(64),x=t(65),O=t(66),f=t(67),v=t(68),N=t(81),A=t(82),S=t(69),z=t(70);var w,k=function(e){var a=r.a.useState(!1),t=Object(g.a)(a,2),s=t[0],i=t[1],c=r.a.useState(!1),o=Object(g.a)(c,2),l=o[0],m=o[1],d=r.a.useState("navbar-transparent"),b=Object(g.a)(d,2),w=b[0],k=b[1];r.a.useEffect((function(){return window.addEventListener("resize",y),function(){window.removeEventListener("resize",y)}}));var y=function(){window.innerWidth<993&&s?k("bg-white"):k("navbar-transparent")},I=function(){m(!l)};return Object(n.jsxs)(n.Fragment,{children:[Object(n.jsx)(j.a,{className:u()("navbar-absolute",w),expand:"lg",children:Object(n.jsxs)(h.a,{fluid:!0,children:[Object(n.jsxs)("div",{className:"navbar-wrapper",children:[Object(n.jsx)("div",{className:u()("navbar-toggle d-inline",{toggled:e.sidebarOpened}),children:Object(n.jsxs)(p.a,{onClick:e.toggleSidebar,children:[Object(n.jsx)("span",{className:"navbar-toggler-bar bar1"}),Object(n.jsx)("span",{className:"navbar-toggler-bar bar2"}),Object(n.jsx)("span",{className:"navbar-toggler-bar bar3"})]})}),Object(n.jsx)(x.a,{href:"#pablo",onClick:function(e){return e.preventDefault()},children:e.brandText})]}),Object(n.jsxs)(p.a,{onClick:function(){k(s?"navbar-transparent":"bg-white"),i(!s)},children:[Object(n.jsx)("span",{className:"navbar-toggler-bar navbar-kebab"}),Object(n.jsx)("span",{className:"navbar-toggler-bar navbar-kebab"}),Object(n.jsx)("span",{className:"navbar-toggler-bar navbar-kebab"})]}),Object(n.jsx)(O.a,{navbar:!0,isOpen:s,children:Object(n.jsxs)(f.a,{className:"ml-auto",navbar:!0,children:[Object(n.jsx)(v.a,{className:"search-bar"}),Object(n.jsx)(N.a,{nav:!0}),Object(n.jsx)("li",{className:"separator d-lg-none"})]})})]})}),Object(n.jsx)(A.a,{modalClassName:"modal-search",isOpen:l,toggle:I,children:Object(n.jsxs)(S.a,{children:[Object(n.jsx)(z.a,{placeholder:"SEARCH",type:"text"}),Object(n.jsx)("button",{"aria-label":"Close",className:"close",onClick:I,children:Object(n.jsx)("i",{className:"tim-icons icon-simple-remove"})})]})})]})},y="blue",I="dark",B=Object(i.createContext)({color:y,changeColor:function(e){}});function M(e){var a=Object(m.g)(),t=r.a.useRef(null);r.a.useEffect((function(){return navigator.platform.indexOf("Win")>-1&&(w=new d.a(t.current,{suppressScrollX:!0,suppressScrollY:!1})),function(){navigator.platform.indexOf("Win")>-1&&w.destroy()}}));var s=e.routes,i=e.rtlActive,c=e.logo,o=null,g=null;return void 0!==c&&(void 0!==c.outterLink?(o=Object(n.jsx)("a",{href:c.outterLink,className:"simple-text logo-mini",target:"/",onClick:e.toggleSidebar,children:Object(n.jsx)("div",{className:"logo-img",children:Object(n.jsx)("img",{src:c.imgSrc,alt:"react-logo"})})}),g=Object(n.jsx)("a",{href:c.outterLink,className:"simple-text logo-normal",target:"/",onClick:e.toggleSidebar,children:c.text})):(o=Object(n.jsx)(l.b,{to:c.innerLink,className:"simple-text logo-mini",onClick:e.toggleSidebar,children:Object(n.jsx)("div",{className:"logo-img",children:Object(n.jsx)("img",{src:c.imgSrc,alt:"react-logo"})})}),g=Object(n.jsx)(l.b,{to:c.innerLink,className:"simple-text logo-normal",onClick:e.toggleSidebar,children:c.text}))),Object(n.jsx)(B.Consumer,{children:function(r){var c=r.color;return Object(n.jsx)("div",{className:"sidebar",data:c,children:Object(n.jsxs)("div",{className:"sidebar-wrapper",ref:t,children:[null!==o||null!==g?Object(n.jsxs)("div",{className:"logo",children:[o,g]}):null,Object(n.jsx)(f.a,{children:s.map((function(t,s){return t.redirect?null:Object(n.jsx)("li",{className:(r=t.path,(a.pathname===r?"active":"")+(t.pro?" active-pro":"")),children:Object(n.jsxs)(l.c,{to:t.layout+t.path,className:"nav-link",activeClassName:"active",onClick:e.toggleSidebar,children:[Object(n.jsx)("i",{className:t.icon}),Object(n.jsx)("p",{children:i?t.rtlName:t.name})]})},s);var r}))})]})})}})}M.defaultProps={rtlActive:!1,routes:[{}]};var L=M,C=t(71),E=t(72),H=t(73),P=t(74),R=t(75),T=t(76),F=t(77);function W(e){return Object(n.jsx)(n.Fragment,{children:Object(n.jsx)("div",{className:"content",children:Object(n.jsx)(C.a,{children:Object(n.jsx)(E.a,{md:"6",children:Object(n.jsxs)(H.a,{children:[Object(n.jsx)(P.a,{children:Object(n.jsx)(R.a,{tag:"h4",children:"Dual-Mag Data Summary"})}),Object(n.jsx)(T.a,{children:Object(n.jsx)(F.a,{className:"tablesorter",responsive:!0,children:Object(n.jsx)("tbody",{children:e.items.map((function(e,a){return Object(n.jsxs)("tr",{children:[Object(n.jsx)("td",{children:e.name}),Object(n.jsx)("td",{children:e.value})]},a)}))})})})]})})})})})}W.defaultProps={items:window.dual_mag_summary};var Y=W,q=t(78),K=t(79);function Q(e){var a=Math.ceil(e.totalItems/e.pageSize),t=[];if(a>e.maxButtons)0===e.pageNumber?(t.push({pageNumber:0,pageName:"0"}),t.push({pageNumber:1,pageName:"Next"}),t.push({pageNumber:a-1,pageName:((a-1)*e.pageSize).toString()})):e.pageNumber===a-1?(t.push({pageNumber:0,pageName:"0"}),t.push({pageNumber:a-2,pageName:"Previous"}),t.push({pageNumber:a-1,pageName:((a-1)*e.pageSize).toString()})):(e.pageNumber>1&&t.push({pageNumber:0,pageName:"0"}),t.push({pageNumber:e.pageNumber-1,pageName:"Previous"}),t.push({pageNumber:e.pageNumber,pageName:(e.pageNumber*e.pageSize).toString()}),t.push({pageNumber:e.pageNumber+1,pageName:"Next"}),e.pageNumber<a-2&&t.push({pageNumber:a-1,pageName:((a-1)*e.pageSize).toString()}));else for(var s=0;s<a;s++)t.push({pageNumber:s,pageName:(s*e.pageSize).toString()});var i=t.map((function(a){return Object(n.jsxs)(q.a,{tag:"label",className:u()("btn-simple",{active:e.pageNumber===a.pageNumber}),color:"info",id:a.pageNumber,size:"sm",onClick:function(){return e.setPageNumber(a.pageNumber)},children:[Object(n.jsx)("span",{className:"d-none d-sm-block d-md-block d-lg-block d-xl-block",children:a.pageName}),Object(n.jsx)("span",{className:"d-block d-sm-none",children:Object(n.jsx)("i",{className:"tim-icons icon-single-02"})})]},a.pageNumber)}));return Object(n.jsx)(n.Fragment,{children:Object(n.jsx)(K.a,{className:"btn-group-toggle float-left","data-toggle":"buttons",children:i})})}Q.defaultProps={maxButtons:6,pageSize:200,totalItems:1e3,pageNumer:0};var U=Q,Z=t(35),D=t.n(Z);t(55);function G(e){var a=r.a.useState(!1),t=Object(g.a)(a,2),s=t[0],i=t[1],c=r.a.useState(0),o=Object(g.a)(c,2),l=o[0],m=o[1],d=[],b=1,u=1;return e.images.length>0&&l<e.images.length?e.isROI?(d=[{src:e.images[l].src,alt:e.images[l].src},{src:e.images[l].src.slice(0,-5)+"_rawcolor.jpeg",alt:e.images[l].src.slice(0,-5)+"_rawcolor.jpeg"},{src:e.images[l].src.slice(0,-5)+"_binary.png",alt:e.images[l].src.slice(0,-5)+"_binary.png"}],b=e.images[l].thumbnailHeight,u=1):(d=e.images.map((function(e){return{src:e.src,alt:e.caption}})),b=e.images[l].fullHeight,u=l):(d=[],b=1),Object(n.jsxs)("div",{children:[Object(n.jsx)(D.a,{visible:s,onClose:function(){i(!1)},images:d,zoomSpeed:.5,minScale:.5,zIndex:1e4,activeIndex:u,defaultScale:window.innerHeight/b,noLimitInitializationSize:!0,imgFilter:"contrast(".concat(e.imageContrast,"%) brightness(").concat(e.imageBrightness,"%)")}),e.images.map((function(a,t){var s=1;s=e.isROI?a.thumbnailWidth:a.fullWidth;var r=a.thumbnailWidth,c=a.thumbnailHeight,o=parseInt(s*e.pixelSize)+" um";return Object(n.jsx)("div",{className:"image-item",style:{backgroundColor:"#050505",width:e.boxSize,height:e.boxSize,overflow:"hidden"},onClick:function(){i(!0),m(t)},children:Object(n.jsx)("div",{style:{filter:"contrast("+e.imageContrast+"%) brightness("+e.imageBrightness+"%)",backgroundImage:"url("+a.thumbnail+")",backgroundPosition:"center",verticalAlign:"center",backgroundSize:"cover",position:"relative",display:"block",width:r>c?e.boxSize-5:r*(e.boxSize-5)/c,height:c>r?e.boxSize-5:c*(e.boxSize-5)/r,margin:"auto",marginTop:c>r?0:e.boxSize/2-c*(e.boxSize-5)/r/2},children:Object(n.jsx)("div",{style:{position:"absolute",bottom:"0",textAlign:"center",width:"100%",borderTop:"1px solid #333"},children:o})})},t)}))]})}G.defaultProps={isROI:!1,imageBrightness:120,imageContrast:150};var J=G,V=t(80);function X(e){return Object(n.jsx)(n.Fragment,{children:Object(n.jsxs)(E.a,{className:e.justify,lg:e.lg,md:e.md,sm:e.sm,children:[Object(n.jsx)("h5",{className:"card-category",children:e.name}),Object(n.jsx)(V.a,{children:Object(n.jsx)(z.a,{type:"select",name:"select",id:e.inputId,onChange:function(a){e.handler(a.target.value)},children:e.items.map((function(a,t){return a===e.value?Object(n.jsx)("option",{id:e.inputId+"_"+t.toString(),selected:!0,children:a}):Object(n.jsx)("option",{id:e.inputId+"_"+t.toString(),children:a})}))})})]})})}X.defaultProps={lg:"12",md:"12",sm:"12",name:"CATEGORY",inputId:"SELECT_ID",justify:"text-left",handler:null,value:0,items:[]};var _=X;function $(e){var a=r.a.useState(0),t=Object(g.a)(a,2),s=t[0],i=t[1],c=r.a.useState(e.pageSize),o=Object(g.a)(c,2),l=o[0],m=o[1],d=r.a.useState(e.sortMethod),b=Object(g.a)(d,2),u=b[0],j=b[1],h=r.a.useState(e.imageContrast),p=Object(g.a)(h,2),x=p[0],O=p[1],f=r.a.useState(e.imageBrightness),v=Object(g.a)(f,2),N=v[0],A=v[1],S=[];return S="Height"===u?e.images.sort((function(e,a){return e.fullHeight>a.fullHeight?-1:1})):"Area"==u?e.images.sort((function(e,a){return e.area>a.area?-1:1})):"Aspect Ratio"==u?e.images.sort((function(e,a){return e.aspectRatio>a.aspectRatio?-1:1})):"Major Axis Length"==u?e.images.sort((function(e,a){return e.majorAxisLength>a.majorAxisLength?-1:1})):e.images.sort((function(e,a){return e.caption>a.caption?-1:1})),Object(n.jsx)(n.Fragment,{children:Object(n.jsx)("div",{className:"content",children:Object(n.jsx)(C.a,{children:Object(n.jsx)(E.a,{children:Object(n.jsxs)(H.a,{className:"card-chart",children:[Object(n.jsxs)(P.a,{children:[Object(n.jsxs)(C.a,{children:[Object(n.jsxs)(E.a,{className:"text-left",lg:"4",md:"0",sm:"0",children:[Object(n.jsx)("h5",{className:"card-category",children:e.title}),Object(n.jsxs)(R.a,{tag:"h2",children:[e.cameraName," ",e.cardTitle]})]}),Object(n.jsx)(_,{justify:"text-left",lg:"2",md:"6",sm:"6",id:"sortMethodSelect",name:"Sort By:",items:e.sortMethodList,handler:j,value:u}),Object(n.jsx)(_,{justify:"text-left",lg:"2",md:"6",sm:"6",id:"pageSizeSelect",name:"Page Size:",items:e.pageSizeList,handler:m,value:l}),Object(n.jsx)(_,{justify:"text-left",lg:"2",md:"6",sm:"6",id:"contrastSelect",name:"Contrast (%):",items:e.contrastList,handler:O,value:x}),Object(n.jsx)(_,{justify:"text-left",lg:"2",md:"6",sm:"6",id:"brightnesstSelect",name:"Brightness (%):",items:e.brightnessList,handler:A,value:N})]}),Object(n.jsx)(C.a,{children:Object(n.jsxs)(E.a,{className:"text-left",sm:"12",children:[Object(n.jsx)("h5",{className:"card-category",children:"Pages: "}),Object(n.jsx)(U,{pageNumber:s,setPageNumber:i,pageSize:l,totalItems:S.length})]})})]}),Object(n.jsx)(T.a,{style:{padding:"10px"},children:Object(n.jsx)("div",{style:{backgroundColor:"#000",borderRadius:"4px",padding:"4px",height:"75vh",overflowY:"scroll"},children:Object(n.jsx)(J,{isROI:e.isROI,images:S.slice(s*l,(s+1)*l),boxSize:200,pixelSize:e.pixelSize,imageContrast:x,imageBrightness:N})})})]})})})})})}$.defaultProps={title:"TITLE",cardTitle:"CARD TITLE",cameraName:"CAMERA NAME",isROI:!1,images:[],pixelSize:6.79,pageSize:200,pageSizeList:[100,200,400,800,1e3,2e3,4e3,1e4],sortMethod:"Height",sortMethodList:["Height","Timestamp"],imageContrast:100,contrastList:[25,50,75,100,115,125,135,150,165,175,185,200],imageBrightness:100,brightnessList:[25,50,75,100,125,150,200,300,400]};var ee=$;function ae(e){return Object(n.jsx)(n.Fragment,{children:Object(n.jsx)(ee,Object(s.a)({},e))})}ae.defaultProps={title:"Detected ROIs",cardTitle:"Camera ROIs",isROI:!0,pageSize:200,cameraName:"Low Mag",images:window.low_mag_cam_rois,pixelSize:6.79,sortMethodList:["Height","Timestamp","Area","Aspect Ratio","Major Axis Length"]};var te=ae;function ne(e){return Object(n.jsx)(n.Fragment,{children:Object(n.jsx)(ee,Object(s.a)({},e))})}ne.defaultProps={title:"Full Frame Images",cardTitle:"Camera Images",isROI:!1,pageSize:200,cameraName:"Low Mag",images:window.low_mag_cam_video,pixelSize:6.79};var se=ne;function ie(e){return Object(n.jsx)(n.Fragment,{children:Object(n.jsx)(ee,Object(s.a)({},e))})}ie.defaultProps={title:"Detected ROIs",cardTitle:"Camera ROIs",isROI:!0,pageSize:200,cameraName:"High Mag",images:window.high_mag_cam_rois,pixelSize:.87,sortMethodList:["Height","Timestamp","Area","Aspect Ratio","Major Axis Length"]};var re=ie;function ce(e){return Object(n.jsx)(n.Fragment,{children:Object(n.jsx)(ee,Object(s.a)({},e))})}ce.defaultProps={title:"Full Frame Images",cardTitle:"Camera Images",isROI:!1,pageSize:200,cameraName:"High Mag",images:window.high_mag_cam_video,pixelSize:.87};var oe,le=[{path:"/summary",name:"Summary",icon:"tim-icons icon-paper",component:Y,layout:"/admin"},{path:"/low-mag-camera-rois",name:"Low Mag Camera ROIs",icon:"tim-icons icon-image-02",component:te,layout:"/admin"},{path:"/low-mag-camera-images",name:"Low Mag Camera Images",icon:"tim-icons icon-image-02",component:se,layout:"/admin"},{path:"/high-mag-camera-rois",name:"High Mag Camera ROIs",icon:"tim-icons icon-image-02",component:re,layout:"/admin"},{path:"/high-mag-camera-images",name:"High Mag Camera Images",icon:"tim-icons icon-image-02",component:ce,layout:"/admin"}];var me=function(e){var a=Object(m.g)(),t=r.a.useRef(null),s=r.a.useState(-1!==document.documentElement.className.indexOf("nav-open")),i=Object(g.a)(s,2),c=i[0],o=i[1];r.a.useEffect((function(){if(navigator.platform.indexOf("Win")>-1){document.documentElement.className+=" perfect-scrollbar-on",document.documentElement.classList.remove("perfect-scrollbar-off"),oe=new d.a(t.current,{suppressScrollX:!0});for(var e=document.querySelectorAll(".table-responsive"),a=0;a<e.length;a++)oe=new d.a(e[a])}return function(){navigator.platform.indexOf("Win")>-1&&(oe.destroy(),document.documentElement.classList.add("perfect-scrollbar-off"),document.documentElement.classList.remove("perfect-scrollbar-on"))}})),r.a.useEffect((function(){if(navigator.platform.indexOf("Win")>-1)for(var e=document.querySelectorAll(".table-responsive"),a=0;a<e.length;a++)oe=new d.a(e[a]);document.documentElement.scrollTop=0,document.scrollingElement.scrollTop=0,t.current&&(t.current.scrollTop=0)}),[a]);var l=function(){document.documentElement.classList.toggle("nav-open"),o(!c)},b=function(e){for(var t=0;t<le.length;t++)if(-1!==a.pathname.indexOf(le[t].layout+le[t].path))return le[t].name;return"Brand"};return Object(n.jsx)(B.Consumer,{children:function(e){var s,i=e.color;e.changeColor;return Object(n.jsx)(r.a.Fragment,{children:Object(n.jsxs)("div",{className:"wrapper",children:[Object(n.jsx)(L,{routes:le,logo:{outterLink:"/",text:"Dual-Mag-01",imgSrc:"data:image/png;base64,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"},toggleSidebar:l}),Object(n.jsxs)("div",{className:"main-panel",ref:t,data:i,children:[Object(n.jsx)(k,{brandText:b(a.pathname),toggleSidebar:l,sidebarOpened:c}),Object(n.jsxs)(m.d,{children:[(s=le,s.map((function(e,a){return"/admin"===e.layout?Object(n.jsx)(m.b,{path:e.layout+e.path,component:e.component},a):null}))),Object(n.jsx)(m.a,{from:"*",to:"/admin/dashboard"})]})]})]})})}})},ge=(t(56),t(57),t(58),t(59),""),de="white-content",be=Object(i.createContext)({theme:ge,changeTheme:function(){}});function ue(e){var a=Object(i.useState)(ge),t=Object(g.a)(a,2),s=t[0],r=t[1];return Object(i.useEffect)((function(){switch(s){case de:document.body.classList.add("white-content");break;case ge:default:document.body.classList.remove("white-content")}}),[s]),Object(n.jsx)(be.Provider,{value:{theme:s,changeTheme:function(e){r(e)}},children:e.children})}function je(e){var a=Object(i.useState)(I),t=Object(g.a)(a,2),s=t[0],r=t[1];return Object(n.jsx)(B.Provider,{value:{color:s,changeColor:function(e){r(e)}},children:e.children})}o.a.render(Object(n.jsx)(ue,{children:Object(n.jsx)(je,{children:Object(n.jsx)(l.a,{children:Object(n.jsxs)(m.d,{children:[Object(n.jsx)(m.b,{path:"/admin",render:function(e){return Object(n.jsx)(me,Object(s.a)({},e))}}),Object(n.jsx)(m.a,{from:"/",to:"/admin/summary"})]})})})}),document.getElementById("root"))}},[[60,1,2]]]);
//# sourceMappingURL=main.5634ebef.chunk.js.map