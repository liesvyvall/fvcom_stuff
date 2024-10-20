% ADD to path, tollbox_liesvy   toolbox_ovel    air-sea-master
% fvcom-tollbox-master

forcing = get_NCEP_forcing_082024(Mobj, [53371, 53374], 'varlist', {'air', 'dlwrf', 'dswrf', ...
    'lhtfl', 'pevpr','prate', 'press', 'rhum', 'shtfl', ...
    'ulwrf', 'uswrf', 'uwnd', 'vwnd'}, 'source', '20thC');
%%
ncinfo('uwnd.10m.2010.nc');
ncdisp('uwnd.10m.2010.nc');
%%
WRF.lon = forcing.lon;
WRF.lat = forcing.lat;
WRF.time = forcing.time;
WRF.nswrs = forcing.nswrs.data;

%nshf = nlwrs + nswrs - lhtfl - shtfl;
WRF.nshf = forcing.nswrs.data + forcing.nlwrs.data - forcing.lhtfl.data - forcing.shtfl.data;
WRF.u10 = forcing.uwnd.data;
WRF.v10 = forcing.vwnd.data;
WRF.P_E = forcing.P_E.data;
WRF.evap = forcing.Et.data;
WRF.pres = forcing.press.data;
WRF.rhum = forcing.rhum.data;
WRF.air = forcing.air.data;
WRF.nlwrs = forcing.nlwrs.data;
WRF.dswrf = forcing.dswrf.data;
WRF.dlwrf = forcing.dlwrf.data;
WRF.uswrf = forcing.uswrf.data;
WRF.ulwrf = forcing.ulwrf.data;
WRF.lhf = forcing.lhtfl.data;
WRF.shf = forcing.shtfl.data;
%%
mean_nswrs_time_domain = mean(WRF.nswrs(:));
mean_nshf_time_domain = mean(WRF.nshf(:));

% CAlcular medias mensuales para cada variable


%%
   windBase = 'gc_blp4.nc';
   write_FVCOM_forcing_082024(Mobj, windBase, forcing, ...
       'FVCOM atmospheric forcing data', '3.1.6');

%%
write_WRF_forcing_hfx(WRF, '2005_wind_hfx4.nc')
