# 88L2 — 31호 LIPT 주모형 재적합, 중강도 PA CrI 5자리(반올림 1.000 해소용, 2026-11-12 신규). 결과 S46b.
#  역방향: 내과 전문의/10만(가설 +, 관측 −).
#  P0 주모형 · P1 +미충족의료·고혈압/당뇨 진단 비중 · P2 단독(+강제) · P3a 의사/1000 제외(같은 축) · P3b 대졸·도시 비중 축 제외 대신 대졸 제외 ·
#  P4 지역 간·지역 내 분해 · P5 면적당(log, 분모 효과) 대체 · P5b 인구당+면적당 동시
#  사용(01_스크립트/): TAG=LIPT ST_VER=std3 ST_GRAPH=<graph_593> ./rslot.sh Rscript 88L_lipt_reverse_posthoc.R → results_std3/S46_lipt_posthoc.csv
suppressPackageStartupMessages({library(INLA);library(sf);library(jsonlite)})
TAG<-Sys.getenv("TAG","LIPT");VER<-Sys.getenv("ST_VER","std3");inla.setOption(num.threads="1:1")
OUTD<-file.path("..","04_분석",TAG);RES<-file.path(OUTD,paste0("results_",VER))
SHP<-Sys.getenv("ST_SHP",file.path(normalizePath(file.path(dirname(sub("--file=","",grep("--file=",commandArgs(),value=TRUE))),"..")),"data","boundary","final.shp"))
S<-fromJSON(file.path(OUTD,sprintf("config_%s_%s.json",TAG,VER)),simplifyVector=TRUE)
DD<-read.csv(file.path(OUTD,sprintf("panel_%s_%s.csv",TAG,VER)),fileEncoding="UTF-8-BOM",stringsAsFactors=FALSE);DD$fbd_region<-enc2utf8(DD$fbd_region)
G<-st_read(SHP,quiet=TRUE);G$region<-enc2utf8(G$region);g<-inla.read.graph(Sys.getenv("ST_GRAPH"));stopifnot(g$n==nrow(G))
DD$area<-match(DD$fbd_region,G$region);DD$time<-DD$year-min(DD$year)+1;DD$yiid<-DD$time
FORCED<-S$forced;HYP<-as.character(S$sets_after_vif$S1_narrative_full)
pc<-list(prec=list(prior="pc.prec",param=c(0.5,0.01)),phi=list(prior="pc",param=c(0.5,2/3)));pcp<-list(prec=list(prior="pc.prec",param=c(0.5,0.01)))
REV<-c("im_specialists_per_100k");EXTRA<-character(0)
z<-function(x)(x-mean(x))/sd(x)
DD$spec_per_km2_log<-z(log1p(DD$im_specialists_per_100k_raw*DD$population/1e5/(DD$area_m2/1e6)))
fit<-function(vars){f<-as.formula(paste("cases ~ 1 +",paste(sprintf("`%s`",vars),collapse="+"),"+ f(area,model='bym2',graph=g,scale.model=TRUE,constr=TRUE,hyper=pc) + f(time,model='rw1',scale.model=TRUE,hyper=pcp) + f(yiid,model='iid',hyper=pcp)"))
  inla(f,family="nbinomial",data=DD,E=DD$E,control.fixed=list(mean=0,prec=4,mean.intercept=0,prec.intercept=0.001),control.compute=list(waic=TRUE),control.inla=list(control.vb=list(emergency=50)))}
out<-NULL
add<-function(an,m,vs){fx<-m$summary.fixed;for(v in vs){if(!v%in%rownames(fx))next;r<-fx[v,];out<<-rbind(out,data.frame(analysis=an,cov=v,IRR=round(exp(r$mean),4),lo=round(exp(r$`0.025quant`),4),hi=round(exp(r$`0.975quant`),4),cred=(exp(r$`0.025quant`)>1|exp(r$`0.975quant`)<1),WAIC=round(m$waic$waic,1)))};cat(an,"done\n")}
MAIN<-unique(c(HYP,FORCED));SENS<-intersect(c("ext__unmet_need_rate","ext__dx_htn_share","ext__dx_dm_share"),names(DD))
V<-"im_specialists_per_100k"
m0<-fit(MAIN)
fx<-m0$summary.fixed;r<-fx["moderate_pa_rate",];write.csv(data.frame(cov="moderate_pa_rate",IRR=exp(r$mean),lo=exp(r$`0.025quant`),hi=exp(r$`0.975quant`)),file.path(RES,"S46b_lipt_mpa_precise.csv"),row.names=FALSE);print(exp(c(r$mean,r$`0.025quant`,r$`0.975quant`)),digits=6)
