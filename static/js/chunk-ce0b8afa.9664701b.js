(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-ce0b8afa"],{"495a":function(t,e,n){},"6eb6":function(t,e,n){"use strict";n("495a")},7636:function(t,e,n){"use strict";n("9c7a")},8312:function(t,e,n){"use strict";n.r(e);var i=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"components-container"},[n("div",{staticClass:"box"},[n("div",[n("div",{staticStyle:{"margin-top":"30px"}},[t._v("标题")]),n("tinymce",{ref:"title",attrs:{toolbar:"",menubar:"",height:50},model:{value:t.title,callback:function(e){t.title=e},expression:"title"}})],1),n("div",{staticStyle:{"margin-top":"30px"}},[n("div",[t._v("内容")]),n("tinymce",{ref:"content",attrs:{height:200},model:{value:t.content,callback:function(e){t.content=e},expression:"content"}})],1),n("div",{staticStyle:{width:"100%","text-align":"center"}},[n("el-button",{staticStyle:{margin:"30px auto"},on:{click:t.reset}},[t._v("重置")]),n("el-button",{staticStyle:{margin:"30px auto"},on:{click:t.submit}},[t._v("提交")])],1)])])},o=[],a=(n("a9e3"),function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"tinymce-container",class:{fullscreen:t.fullscreen},style:{width:t.containerWidth}},[n("textarea",{staticClass:"tinymce-textarea",attrs:{id:t.tinymceId}}),t._v(" "),n("div",{staticClass:"editor-custom-btn-container"},[n("editorImage",{staticClass:"editor-upload-btn",attrs:{color:"#1890ff"},on:{successCBK:t.imageSuccessCBK}})],1)])}),s=[],c=(n("b680"),n("159b"),function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"upload-container"},[n("el-button",{style:{background:t.color,borderColor:t.color},attrs:{icon:"el-icon-upload",size:"mini",type:"primary"},on:{click:function(e){t.dialogVisible=!0}}},[t._v(" upload ")]),n("el-dialog",{attrs:{visible:t.dialogVisible},on:{"update:visible":function(e){t.dialogVisible=e}}},[n("el-upload",{staticClass:"editor-slide-upload",attrs:{multiple:!0,"file-list":t.fileList,"show-file-list":!0,"on-remove":t.handleRemove,"on-success":t.handleSuccess,"on-error":t.hanldeError,"before-upload":t.beforeUpload,headers:{token:t.token},action:"http://192.168.2.103:9200/api/uploadImg","list-type":"picture-card"}},[n("el-button",{attrs:{size:"small",type:"primary"}},[t._v(" 点击上传 ")])],1),n("el-button",{on:{click:function(e){t.dialogVisible=!1}}},[t._v(" 取消 ")]),n("el-button",{attrs:{type:"primary"},on:{click:t.handleSubmit}},[t._v(" 确定 ")])],1)],1)}),r=[],l=(n("b64b"),n("d81d"),n("2b3d"),n("d3b7"),n("3ca3"),n("ddb0"),n("5f87")),u=n("83d6"),d=n.n(u),h={name:"EditorSlideUpload",props:{color:{type:String,default:"#1890ff"}},data:function(){return{dialogVisible:!1,listObj:{},fileList:[],token:Object(l["a"])(),baseUrl:d.a.baserUrl}},methods:{checkAllSuccess:function(){var t=this;return Object.keys(this.listObj).every((function(e){return t.listObj[e].hasSuccess}))},handleSubmit:function(){var t=this,e=Object.keys(this.listObj).map((function(e){return t.listObj[e]}));this.checkAllSuccess()?(this.$emit("successCBK",e),this.listObj={},this.fileList=[],this.dialogVisible=!1):this.$message("请等待上传完成")},hanldeError:function(t){console.info("上传失败",t)},handleSuccess:function(t,e){var n=e.uid,i=Object.keys(this.listObj);if(0==t.code){for(var o=0,a=i.length;o<a;o++)if(this.listObj[i[o]].uid===n)return this.listObj[i[o]].url=t.data.src,void(this.listObj[i[o]].hasSuccess=!0)}else this.$message.error(t.data.msg||"上传失败")},handleRemove:function(t){for(var e=t.uid,n=Object.keys(this.listObj),i=0,o=n.length;i<o;i++)if(this.listObj[n[i]].uid===e)return void delete this.listObj[n[i]]},beforeUpload:function(t){var e=this,n=window.URL||window.webkitURL,i=t.uid;return this.listObj[i]={},new Promise((function(o,a){var s=new Image;s.src=n.createObjectURL(t),s.onload=function(){e.listObj[i]={hasSuccess:!1,uid:t.uid,width:this.width,height:this.height}},o(!0)}))}}},f=h,m=(n("6eb6"),n("2877")),b=Object(m["a"])(f,c,r,!1,null,"7dbb55fe",null),p=b.exports,g=["advlist anchor autolink autosave code codesample colorpicker colorpicker contextmenu directionality emoticons fullscreen hr image imagetools insertdatetime link lists media nonbreaking noneditable pagebreak paste preview print save searchreplace spellchecker tabfocus table template textcolor textpattern visualblocks visualchars wordcount"],y=g,v=["searchreplace bold italic underline strikethrough alignleft aligncenter alignright outdent indent  blockquote undo redo removeformat subscript superscript code codesample","hr bullist numlist link image charmap preview anchor pagebreak insertdatetime media table emoticons forecolor backcolor fullscreen","fontselect fontsizeselect"],w=v,_=n("b85c"),k=[];function j(){return window.tinymce}var C=function(t,e){var n=document.getElementById(t),i=e||function(){};if(!n){var o=document.createElement("script");o.src=t,o.id=t,document.body.appendChild(o),k.push(i);var a="onload"in o?s:c;a(o)}function s(e){e.onload=function(){this.onerror=this.onload=null;var t,n=Object(_["a"])(k);try{for(n.s();!(t=n.n()).done;){var i=t.value;i(null,e)}}catch(o){n.e(o)}finally{n.f()}k=null},e.onerror=function(){this.onerror=this.onload=null,i(new Error("Failed to load "+t),e)}}function c(t){t.onreadystatechange=function(){if("complete"===this.readyState||"loaded"===this.readyState){this.onreadystatechange=null;var e,n=Object(_["a"])(k);try{for(n.s();!(e=n.n()).done;){var i=e.value;i(null,t)}}catch(o){n.e(o)}finally{n.f()}k=null}}}n&&i&&(j()?i(null,n):k.push(i))},O=C,S="https://cdn.jsdelivr.net/npm/tinymce-all-in-one@4.9.3/tinymce.min.js",x={name:"Tinymce",components:{editorImage:p},props:{id:{type:String,default:function(){return"vue-tinymce-"+ +new Date+(1e3*Math.random()).toFixed(0)}},value:{type:String,default:""},toolbar:{type:Array,required:!1,default:function(){return[]}},menubar:{type:String,default:"file edit insert view format table"},height:{type:[Number,String],required:!1,default:360},width:{type:[Number,String],required:!1,default:"auto"}},data:function(){return{hasChange:!1,hasInit:!1,tinymceId:this.id,fullscreen:!1,languageTypeList:{en:"en",zh:"zh_CN",es:"es_MX",ja:"ja"}}},computed:{containerWidth:function(){var t=this.width;return/^[\d]+(\.[\d]+)?$/.test(t)?"".concat(t,"px"):t}},watch:{value:function(t){var e=this;!this.hasChange&&this.hasInit&&this.$nextTick((function(){return window.tinymce.get(e.tinymceId).setContent(t||"")}))}},mounted:function(){this.init()},activated:function(){window.tinymce&&this.initTinymce()},deactivated:function(){this.destroyTinymce()},destroyed:function(){this.destroyTinymce()},methods:{init:function(){var t=this;O(S,(function(e){e?t.$message.error(e.message):t.initTinymce()}))},initTinymce:function(){var t=this,e=this;window.tinymce.init({selector:"#".concat(this.tinymceId),language:this.languageTypeList["zh"],height:this.height,fontsize_formats:"8pt 10pt 12pt 14pt 18pt 24pt 36pt",body_class:"panel-body ",object_resizing:!1,toolbar:this.toolbar.length>0?this.toolbar:w,menubar:this.menubar,plugins:y,end_container_on_empty_block:!0,powerpaste_word_import:"clean",code_dialog_height:450,code_dialog_width:1e3,advlist_bullet_styles:"square",advlist_number_styles:"default",imagetools_cors_hosts:["www.tinymce.com","codepen.io"],default_link_target:"_blank",link_title:!1,nonbreaking_force_tab:!0,init_instance_callback:function(n){e.value&&n.setContent(e.value),e.hasInit=!0,n.on("NodeChange Change KeyUp SetContent",(function(){t.hasChange=!0,t.$emit("input",n.getContent())}))},setup:function(t){t.on("FullscreenStateChanged",(function(t){e.fullscreen=t.state}))},convert_urls:!1})},destroyTinymce:function(){var t=window.tinymce.get(this.tinymceId);this.fullscreen&&t.execCommand("mceFullScreen"),t&&t.destroy()},setContent:function(t){window.tinymce.get(this.tinymceId).setContent(t)},getContent:function(){window.tinymce.get(this.tinymceId).getContent()},imageSuccessCBK:function(t){var e=this;t.forEach((function(t){return window.tinymce.get(e.tinymceId).insertContent('<img class="wscnph" src="'.concat(t.url,'" >'))}))}}},I=x,$=(n("ddcb"),Object(m["a"])(I,a,s,!1,null,"c59af172",null)),T=$.exports,E=n("ad8f"),U={name:"add",props:{id:{type:Number,default:0}},components:{Tinymce:T},created:function(){},data:function(){return{title:"",content:""}},mounted:function(){this.getDate()},methods:{reset:function(){this.title="",this.content="",this.$refs.title.setContent(""),this.$refs.content.setContent("")},getDate:function(){var t=this;this.id&&Object(E["b"])({id:this.id}).then((function(e){t.title=e.data.title,t.content=e.data.content,t.$refs.title.setContent(e.data.title),t.$refs.content.setContent(e.data.content)})).catch((function(t){console.info("err",t)}))},submit:function(){var t=this;Object(E["d"])({id:this.id,title:this.title,content:this.content}).then((function(e){console.info("data===",e),t.id?(t.$message.success("修改成功"),t.$router.go(-1)):(t.$message.success("创建成功"),t.reset())}))}}},z=U,L=(n("7636"),Object(m["a"])(z,i,o,!1,null,"3377c68c",null));e["default"]=L.exports},"9c7a":function(t,e,n){},"9e94":function(t,e,n){},ad8f:function(t,e,n){"use strict";n.d(e,"c",(function(){return o})),n.d(e,"a",(function(){return a})),n.d(e,"b",(function(){return s})),n.d(e,"d",(function(){return c}));var i=n("b775");function o(t){return Object(i["a"])({url:"/tie",method:"get",params:t})}function a(t){return Object(i["a"])({url:"/tie",method:"delete",data:t})}function s(t){return Object(i["a"])({url:"/tieInfo",method:"get",params:t})}function c(t){return Object(i["a"])({url:"/tie",method:"put",data:t})}},ddcb:function(t,e,n){"use strict";n("9e94")}}]);