Search.setIndex({docnames:["crawler_api","crawler_cli","design","documentation","index"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,"sphinx.ext.viewcode":1,sphinx:56},filenames:["crawler_api.rst","crawler_cli.rst","design.md","documentation.md","index.md"],objects:{"crawler-registry":[[1,9,1,"cmdoption-crawler-registry-get-catalog","--get-catalog"],[1,9,1,"cmdoption-crawler-registry-get-catalogs","--get-catalogs"],[1,9,1,"cmdoption-crawler-registry-get-collection","--get-collection"],[1,9,1,"cmdoption-crawler-registry-get-collections","--get-collections"],[1,9,1,"cmdoption-crawler-registry-id","--id"],[1,9,1,"cmdoption-crawler-registry-get-catalog","--no-get-catalog"],[1,9,1,"cmdoption-crawler-registry-get-catalogs","--no-get-catalogs"],[1,9,1,"cmdoption-crawler-registry-get-collection","--no-get-collection"],[1,9,1,"cmdoption-crawler-registry-get-collections","--no-get-collections"],[1,9,1,"cmdoption-crawler-registry-path","--path"]],"crawler-schemas":[[1,9,1,"cmdoption-crawler-schemas-get","--get"],[1,9,1,"cmdoption-crawler-schemas-name","--name"],[1,9,1,"cmdoption-crawler-schemas-get","--no-get"],[1,9,1,"cmdoption-crawler-schemas-type","--type"]],"crawler.crawler":[[0,1,1,"","Crawler"]],"crawler.crawler.Crawler":[[0,2,1,"","extract_collection"],[0,2,1,"","get_registered_collections"],[0,2,1,"","get_registered_services"],[0,2,1,"","get_source_collection"],[0,2,1,"","get_source_collections"],[0,2,1,"","ingest_collection"],[0,2,1,"","list_source_collections"],[0,2,1,"","reset_datastore"],[0,2,1,"","retrieve_registered_collections"],[0,2,1,"","retrieve_registered_services"],[0,2,1,"","save_registered_collections"],[0,2,1,"","transform_collection"]],"crawler.extractor":[[0,1,1,"","AbstractExtractor"],[0,1,1,"","EPNTAP_Extractor"],[0,3,1,"","EXTRACTORS"],[0,4,1,"","Extractor"],[0,1,1,"","PDSODE_Extractor"],[0,1,1,"","WFS_Extractor"]],"crawler.extractor.AbstractExtractor":[[0,2,1,"","extract"],[0,2,1,"","get_service_collections"],[0,2,1,"","set_service"]],"crawler.extractor.PDSODE_Extractor":[[0,2,1,"","extract"],[0,2,1,"","get_collection_metadata"],[0,2,1,"","get_service_collections"],[0,2,1,"","read_collection_metadata"],[0,2,1,"","read_next_product_metadata"],[0,2,1,"","reset_reader_iterator"],[0,2,1,"","retrieve_service_collections"]],"crawler.ingestor":[[0,1,1,"","Ingestor"]],"crawler.registry":[[0,5,1,"","ExternalService"],[0,1,1,"","ExternalServiceType"],[0,1,1,"","HealthcheckrRegistry"],[0,1,1,"","LocalRegistry"],[0,1,1,"","ProviderRole"],[0,1,1,"","RegistryInterface"],[0,5,1,"","Service"],[0,5,1,"","ServiceProvider"],[0,1,1,"","ServiceType"]],"crawler.registry.ExternalService":[[0,6,1,"","extra_params"],[0,6,1,"","type"]],"crawler.registry.ExternalServiceType":[[0,7,1,"","EPNTAP"],[0,7,1,"","PDSODE"],[0,7,1,"","WFS"]],"crawler.registry.HealthcheckrRegistry":[[0,2,1,"","get_services"]],"crawler.registry.LocalRegistry":[[0,2,1,"","get_services"]],"crawler.registry.ProviderRole":[[0,7,1,"","host"],[0,7,1,"","licensor"],[0,7,1,"","processor"],[0,7,1,"","producer"]],"crawler.registry.RegistryInterface":[[0,2,1,"","get_services"]],"crawler.registry.Service":[[0,6,1,"","description"],[0,6,1,"","ping_url"],[0,6,1,"","providers"],[0,6,1,"","ssys_targets"],[0,6,1,"","title"],[0,6,1,"","type"],[0,6,1,"","url"]],"crawler.registry.ServiceProvider":[[0,6,1,"","description"],[0,6,1,"","name"],[0,6,1,"","roles"],[0,6,1,"","url"]],"crawler.registry.ServiceType":[[0,7,1,"","STAC"],[0,7,1,"","WFS"],[0,7,1,"","WMS"],[0,7,1,"","WMTS"],[0,7,1,"","XYZ"]],"crawler.schemas":[[0,5,1,"","EPNTAP_Granule"],[0,5,1,"","MARSSI_WFS_Feature"],[0,5,1,"","PDSODE_Product"],[0,5,1,"","PDSODE_Product_file"],[0,5,1,"","PDSSP_STAC_Assets"],[0,5,1,"","PDSSP_STAC_Collection"],[0,5,1,"","PDSSP_STAC_Extent"],[0,5,1,"","PDSSP_STAC_Item"],[0,5,1,"","PDSSP_STAC_Link"],[0,5,1,"","PDSSP_STAC_Properties"],[0,5,1,"","PDSSP_STAC_Provider"],[0,5,1,"","PDSSP_STAC_SpatialExtent"],[0,5,1,"","PDSSP_STAC_TemporalExtent"],[0,4,1,"","create_schema_object"],[0,4,1,"","get_schema_json"],[0,4,1,"","get_schema_names"]],"crawler.schemas.EPNTAP_Granule":[[0,6,1,"","access_estsize"],[0,6,1,"","access_format"],[0,6,1,"","access_url"],[0,6,1,"","c1_resol_max"],[0,6,1,"","c1_resol_min"],[0,6,1,"","c1max"],[0,6,1,"","c1min"],[0,6,1,"","c2_resol_max"],[0,6,1,"","c2_resol_min"],[0,6,1,"","c2max"],[0,6,1,"","c2min"],[0,6,1,"","c3_resol_max"],[0,6,1,"","c3_resol_min"],[0,6,1,"","c3max"],[0,6,1,"","c3min"],[0,6,1,"","creation_date"],[0,6,1,"","dataproduct_type"],[0,6,1,"","emergence_max"],[0,6,1,"","emergence_min"],[0,6,1,"","file_name"],[0,6,1,"","granule_gid"],[0,6,1,"","granule_uid"],[0,6,1,"","incidence_max"],[0,6,1,"","incidence_min"],[0,6,1,"","instrument_host_name"],[0,6,1,"","instrument_name"],[0,6,1,"","measurement_type"],[0,6,1,"","modification_date"],[0,6,1,"","obs_id"],[0,6,1,"","phase_max"],[0,6,1,"","phase_min"],[0,6,1,"","processing_level"],[0,6,1,"","publisher"],[0,6,1,"","release_date"],[0,6,1,"","s_region"],[0,6,1,"","service_title"],[0,6,1,"","spatial_frame_type"],[0,6,1,"","spectral_range_max"],[0,6,1,"","spectral_range_min"],[0,6,1,"","spectral_resolution_max"],[0,6,1,"","spectral_resolution_min"],[0,6,1,"","spectral_sampling_step_max"],[0,6,1,"","spectral_sampling_step_min"],[0,6,1,"","target_class"],[0,6,1,"","target_name"],[0,6,1,"","time_exp_max"],[0,6,1,"","time_exp_min"],[0,6,1,"","time_max"],[0,6,1,"","time_min"],[0,6,1,"","time_sampling_step_max"],[0,6,1,"","time_sampling_step_min"]],"crawler.schemas.PDSODE_Product":[[0,6,1,"","Data_set_id"],[0,6,1,"","LabelFileName"],[0,6,1,"","Label_Product_Type"],[0,6,1,"","Observation_id"],[0,6,1,"","PDSVolume_id"],[0,6,1,"","Product_creation_time"],[0,6,1,"","Product_files"],[0,6,1,"","Product_version_id"],[0,6,1,"","RelativePathtoVol"],[0,6,1,"","Target_name"],[0,6,1,"","ihid"],[0,6,1,"","iid"],[0,6,1,"","ode_id"],[0,6,1,"","pdsid"],[0,6,1,"","pt"]],"crawler.schemas.PDSODE_Product_file":[[0,6,1,"","Description"],[0,6,1,"","FileName"],[0,6,1,"","KBytes"],[0,6,1,"","Type"],[0,6,1,"","URL"]],"crawler.schemas.PDSSP_STAC_Assets":[[0,6,1,"","description"],[0,6,1,"","href"],[0,6,1,"","roles"],[0,6,1,"","title"],[0,6,1,"","type"]],"crawler.schemas.PDSSP_STAC_Collection":[[0,6,1,"","assets"],[0,6,1,"","description"],[0,6,1,"","extent"],[0,6,1,"","id"],[0,6,1,"","keywords"],[0,6,1,"","licence"],[0,6,1,"","links"],[0,6,1,"","providers"],[0,6,1,"","stac_extensions"],[0,6,1,"","stac_version"],[0,6,1,"","summaries"],[0,6,1,"","title"],[0,6,1,"","type"]],"crawler.schemas.PDSSP_STAC_Extent":[[0,6,1,"","spatial"],[0,6,1,"","temporal"]],"crawler.schemas.PDSSP_STAC_Item":[[0,6,1,"","assets"],[0,6,1,"","bbox"],[0,6,1,"","collection"],[0,6,1,"","geometry"],[0,6,1,"","id"],[0,6,1,"","links"],[0,6,1,"","properties"],[0,6,1,"","stac_extensions"],[0,6,1,"","stac_version"],[0,6,1,"","type"]],"crawler.schemas.PDSSP_STAC_Link":[[0,6,1,"","href"],[0,6,1,"","rel"],[0,6,1,"","title"],[0,6,1,"","type"]],"crawler.schemas.PDSSP_STAC_Properties":[[0,6,1,"","constellation"],[0,6,1,"","created"],[0,6,1,"","datetime"],[0,6,1,"","description"],[0,6,1,"","end_datetime"],[0,6,1,"","gsd"],[0,6,1,"","instruments"],[0,6,1,"","license"],[0,6,1,"","mission"],[0,6,1,"","platform"],[0,6,1,"","ssys_easternmost_longitude"],[0,6,1,"","ssys_targets"],[0,6,1,"","ssys_westernmost_longitude"],[0,6,1,"","start_datetime"],[0,6,1,"","title"],[0,6,1,"","updated"]],"crawler.schemas.PDSSP_STAC_Provider":[[0,6,1,"","description"],[0,6,1,"","name"],[0,6,1,"","roles"]],"crawler.schemas.PDSSP_STAC_SpatialExtent":[[0,6,1,"","bbox"]],"crawler.schemas.PDSSP_STAC_TemporalExtent":[[0,6,1,"","interval"]],"crawler.transformer":[[0,1,1,"","AbstractTransformer"],[0,1,1,"","EPNTAP_STAC"],[0,1,1,"","MARSSI_STAC"],[0,1,1,"","PDSODE_STAC"],[0,4,1,"","Transformer"],[0,8,1,"","TransformerSchemaInputError"]],"crawler.transformer.AbstractTransformer":[[0,2,1,"","transform_source_file"],[0,2,1,"","transform_source_metadata"]],"crawler.transformer.PDSODE_STAC":[[0,2,1,"","get_stac_item_dict"],[0,2,1,"","transform_source_metadata"]],crawler:[[0,0,0,"-","crawler"],[0,0,0,"-","extractor"],[0,0,0,"-","ingestor"],[0,0,0,"-","registry"],[0,0,0,"-","schemas"],[0,0,0,"-","transformer"],[1,9,1,"cmdoption-crawler-version","--version"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","data","Python data"],"4":["py","function","Python function"],"5":["py","pydantic_model","Python model"],"6":["py","pydantic_field","Python field"],"7":["py","attribute","Python attribute"],"8":["py","exception","Python exception"],"9":["std","cmdoption","program option"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:data","4":"py:function","5":"py:pydantic_model","6":"py:pydantic_field","7":"py:attribute","8":"py:exception","9":"std:cmdoption"},terms:{"0":0,"1":0,"2022":2,"29":0,"8":2,"abstract":0,"class":[0,2],"default":0,"enum":0,"float":0,"function":0,"import":3,"new":0,"return":0,"super":0,"true":0,A:0,The:0,To:0,__init__:0,_build:3,absolut:0,abstractextractor:0,abstracttransform:0,access:0,access_ests:0,access_format:0,access_url:0,act:0,actual:0,add:0,airflow:0,alia:0,all:0,allow:0,an:0,ani:0,api:4,ar:0,arg:1,arrai:0,asset:0,associ:0,avail:0,base:0,basemodel:0,basic:0,bbox:0,between:0,blob:0,book:3,both:0,build:3,c1:0,c1_resol_max:0,c1_resol_min:0,c1max:0,c1min:0,c2:0,c2_resol_max:0,c2_resol_min:0,c2max:0,c2min:0,c3:0,c3_resol_max:0,c3_resol_min:0,c3max:0,c3min:0,can:0,catalog:[0,1],children:0,cli:[0,4],collect:[0,1],collection_id:0,collection_metadata_file_path:0,com:0,command:1,common:0,commonmark:0,compliant:0,constel:0,contact:0,control:0,correspond:0,cover:0,crawler:3,creat:0,create_schema_object:0,creation:0,creation_d:0,current:0,custom:0,dag:0,data:0,data_set_id:0,dataproduct:0,dataproduct_typ:0,datastor:0,date:0,datetim:0,dec:2,def:0,defin:0,definit:0,descript:0,design:4,destin:0,destination_schema:0,detail:0,diagram:2,dict:0,differ:0,directori:3,displai:0,doc:3,document:0,dst_file_path:0,easternmost:0,emerg:0,emergence_max:0,emergence_min:0,end:0,end_datetim:0,entiti:0,enumer:0,epn:0,epntap:0,epntap_collect:0,epntap_extractor:0,epntap_granul:0,epntap_stac:0,error:0,estsiz:0,exampl:0,except:0,exist:0,exit:1,exp:0,extens:0,extent:0,extern:[0,2],externalservic:0,externalservicetyp:0,extra:0,extra_param:0,extract:0,extract_collect:0,extracted_fil:0,f:3,factori:0,fals:0,featur:0,field:0,file:0,file_nam:0,filenam:0,filter:[0,1],format:0,fr:0,frame:0,from:[0,3],further:0,geometri:0,get:1,get_collection_metadata:0,get_registered_collect:0,get_registered_servic:0,get_schema_json:0,get_schema_nam:0,get_servic:0,get_service_collect:0,get_source_collect:0,get_stac_item_dict:0,ghp:3,gid:0,github:0,given:0,granul:0,granule_gid:0,granule_uid:0,gsd:0,handl:0,healthcheckrregistri:0,high:0,homepag:0,host:0,href:0,html:3,http:0,human:0,ia:0,id:[0,1],identifi:0,ihid:0,iid:0,incid:0,incidence_max:0,incidence_min:0,index:0,individu:0,inform:[0,1],ingest:0,ingest_collect:0,input:0,instrument:0,instrument_host_nam:0,instrument_nam:0,interfac:[0,2],intern:0,interv:0,invalid:0,item:[0,1],iter:0,ivoa:0,json:[0,1],jupyt:3,kbyte:0,keyword:0,label:0,label_product_typ:0,labelfilenam:0,latest:2,level:0,licenc:0,licens:0,licensor:0,line:0,link:0,list:[0,1],list_source_collect:0,local:0,localregistri:0,longitud:0,mai:0,main:0,mar:0,marssi:0,marssi_stac:0,marssi_wfs_featur:0,marssi_wfs_lay:0,master:0,match:0,max:0,md:0,measur:0,measurement_typ:0,media:0,metadata:0,min:0,mission:0,model:0,modif:0,modification_d:0,multi:0,n:3,name:[0,1],new_extractor:0,next:0,none:0,number:0,ob:0,object:[0,1],object_typ:0,obs_id:0,observ:0,observation_id:0,od:0,ode_id:0,ode_product_typ:0,option:[0,1],organ:0,output_dir_path:0,overwrit:0,p:3,packag:3,param:0,paramet:0,pari:0,pass:0,path:[0,1],pd:0,pdsid:0,pdsode:0,pdsode_extractor:0,pdsode_product:0,pdsode_product_fil:0,pdsode_stac:0,pdssp:[0,3],pdssp_stac:0,pdssp_stac_asset:0,pdssp_stac_catalog:0,pdssp_stac_collect:0,pdssp_stac_ext:0,pdssp_stac_item:0,pdssp_stac_link:0,pdssp_stac_properti:0,pdssp_stac_provid:0,pdssp_stac_spatialext:0,pdssp_stac_temporalext:0,pdsvolum:0,pdsvolume_id:0,phase:0,phase_max:0,phase_min:0,ping:0,ping_url:0,platform:[0,4],point:0,potenti:0,process:0,processing_level:0,processor:0,produc:0,product:0,product_creation_tim:0,product_fil:0,product_version_id:0,properti:0,provid:0,providerrol:0,pt:0,publish:0,pydant:0,python:4,radiantearth:0,rais:0,rang:0,read:0,read_collection_metadata:0,read_next_product_metadata:0,readabl:0,reader:0,record:0,ref:0,refer:0,referenc:0,region:0,registryinterfac:0,rel:0,relationship:0,relativepathtovol:0,releas:0,release_d:0,render:0,repres:0,represent:[0,1],requir:0,reset:0,reset_datastor:0,reset_reader_iter:0,resol:0,resolut:0,result:0,retriev:0,retrieve_registered_collect:0,retrieve_registered_servic:0,retrieve_service_collect:0,rich:0,role:0,root:0,s:0,s_region:0,saclai:0,sampl:0,save_registered_collect:0,scientif:0,self:0,serv:0,servic:0,service_titl:0,service_typ:0,serviceprovid:0,servicetyp:0,set:0,set_servic:0,show:[0,1],sourc:0,source_schema:0,sourcecollectionmodel:0,spatial:0,spatial_frame_typ:0,spec:0,spectral:0,spectral_range_max:0,spectral_range_min:0,spectral_resolution_max:0,spectral_resolution_min:0,spectral_sampling_step_max:0,spectral_sampling_step_min:0,src_file_path:0,src_metadata:0,ssy:0,ssys_easternmost_longitud:0,ssys_target:0,ssys_westernmost_longitud:0,stac:0,stac_extens:0,stac_vers:0,start:0,start_datetim:0,std:0,step:0,str:0,string:0,summari:0,syntax:0,tap:0,target:0,target_class:0,target_nam:0,tempor:0,text:0,time:0,time_exp_max:0,time_exp_min:0,time_max:0,time_min:0,time_sampling_step_max:0,time_sampling_step_min:0,titl:0,transform_collect:0,transform_source_fil:0,transform_source_metadata:0,transformerschemainputerror:0,type:[0,1],uid:0,under:4,universit:0,updat:[0,2],url:0,us:0,utc:0,valid_footprint:0,valu:0,version:[0,1],volum:0,westernmost:0,wf:0,wfs_extractor:0,when:0,within:0,wm:0,wmt:0,xml:0,xyz:0},titles:["Crawler Python API","Crawler CLI","Design","Documentation","PDSSP Crawler Documentation"],titleterms:{api:0,cli:1,crawler:[0,1,4],design:2,develop:4,document:[3,4],extractor:0,gener:3,guid:4,ingestor:0,modul:0,pdssp:4,publish:3,python:0,refer:4,registri:[0,1],schema:[0,1],store:0,transform:0}})