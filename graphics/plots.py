# %%
# from os import sep
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# import plotly.io as pio
# # pio.renderers = 'svg'
# import chart_studio.plotly as py


# %%
def phi_perm_plot(df,**kwargs):
    if 'color' not in kwargs.keys():
        data_temp=[go.Scatter(x=df[kwargs['x_name']].values,
                        y=df[kwargs['y_name']].values,
                        mode='markers',
                        name='All Data'
                        )]
    else:
        data_temp=[go.Scatter(x=df[df[kwargs['color']]==i][kwargs['x_name']].values,
                        y=df[df[kwargs['color']]==i][kwargs['y_name']].values,
                        mode='markers',
                        name=str(i)
                        ) for i in df[kwargs['color']].unique()]
    
    # print(data_temp)
    phi_perm_fig = go.Figure(
        data=data_temp,
        layout=go.Layout(
            title=dict(text=str(kwargs['x_name'])+'-'+str(kwargs['y_name'])),
            xaxis=dict(title='Porosity, %',
                        range=kwargs['x_range'],
                        showline=True,
                        linewidth=2,
                        linecolor='#00008B'),
            yaxis=dict(type='log',
                        title='Permeability_Kl, mD',
                        range=kwargs['y_range'],
                        showline=True,
                        linewidth=2,
                        linecolor='#00008B'
                        ),
            margin={'l': 20, 'b': 20, 't': 40, 'r': 20},
            # margin=dict(l=20, b=20, t=40, r=20),
            showlegend=True,
            template='plotly_white',
            height=400,
            width=600
            )
    )
    return phi_perm_fig

# %%
def cp_sw_plot(df_cp,**kwargs):
    colorsList=px.colors.qualitative.Dark24
    if 'legendgroup' not in kwargs.keys():

        data_cp_temp=[go.Scatter(x=df_cp[(df_cp[kwargs['wells']] == w) & (df_cp[kwargs['sampleID']] == s)][kwargs['x_name']].values,
                                y=df_cp[(df_cp[kwargs['wells']] == w) & (df_cp[kwargs['sampleID']] == s)][kwargs['y_name']].values,
                                mode='markers+lines',
                                name=str(int(s))      
                ) for w in df_cp[kwargs['wells']].unique() for s in df_cp[kwargs['sampleID']].unique()]
    # print(list(data_cp_temp))
    else:
        data_cp_temp=[go.Scatter(x=df_cp[(df_cp[kwargs['legendgroup']] == lgroup) & (df_cp[kwargs['sampleID']] == s)][kwargs['x_name']].values,
                                y=df_cp[(df_cp[kwargs['legendgroup']] == lgroup) & (df_cp[kwargs['sampleID']] == s)][kwargs['y_name']].values,
                                mode='markers+lines',
                                marker=dict(color=colorsList[i]),
                                legendgroup=str(lgroup),
                                name=str(lgroup)+'_'+str(s),      
                ) for i,lgroup in enumerate(df_cp[kwargs['legendgroup']].unique()) \
                for s in df_cp[df_cp[kwargs['legendgroup']]==lgroup][kwargs['sampleID']].unique()]
    #     data_temp=[]
    #     for i,lgroup in enumerate(df_cp[kwargs['legendgroup']].unique()):
    #         for s in df_cp[df[kwargs['legendgroup']]==lgroup][kwargs['sampleID']].unique():
    #             data_temp.append(go.Scatter(
    #                     x=df_cp[(df_cp[kwargs['legendgroup']] == lgroup) & (df_cp[kwargs['sampleID']] == s)][kwargs['x_name']].values,
    #                     y=df_cp[(df_cp[kwargs['legendgroup']] == lgroup) & (df_cp[kwargs['sampleID']] == s)][kwargs['y_name']].values,
    #                     mode='markers+lines',
    #                     marker=dict(color=colorsList[i]),
    #                     legendgroup=str(lgroup),
    #                     name=str(lgroup)+'_'+str(s),      
    #                     )
    #             ),
    # print(data_cp_temp)
    cp_sw_fig = go.Figure(
        # data=[],
        data=list(data_cp_temp),
        layout=go.Layout(
            title=dict(text='Pc-Water Saturation'),
            xaxis=dict(title='Water Saturation, %',
                    range=kwargs['x_range'],
                    showline=True,
                    linewidth=2,
                    linecolor='#00008B'),
            yaxis=dict(
                # type='log',
                title='Pc, atm',
                range=kwargs['y_range'],
                showline=True,
                linewidth=2,
                linecolor='#00008B'
            ),
            margin={'l': 20, 'b': 20, 't': 40, 'r': 20},
            template='plotly_white',
            height=400,
            width=500
            )
    )
    # if 'legendgroup' not in kwargs.keys():
    #    for i,w in enumerate(df_cp[kwargs['wells']].unique()):
    #         for s in df_cp[df_cp[kwargs['wells']]==w][kwargs['sampleID']].unique():
    #             cp_sw_fig.add_trace(go.Scatter(
    #                     x=df_cp[(df_cp[kwargs['wells']] == w) & (df_cp[kwargs['sampleID']] == s)][kwargs['x_name']].values,
    #                     y=df_cp[(df_cp[kwargs['wells']] == w) & (df_cp[kwargs['sampleID']] == s)][kwargs['y_name']].values,
    #                     mode='markers+lines',
    #                     # marker=dict(color=colorsList[i]),
    #                     # legendgroup=str(w),
    #                     name=str(s),      
    #                     )
    #             )
    # else:
    #     for i,lgroup in enumerate(df_cp[kwargs['legendgroup']].unique()):
    #         for s in df_cp[df_cp[kwargs['legendgroup']]==lgroup][kwargs['sampleID']].unique():
    #             cp_sw_fig.add_trace(go.Scatter(
    #                     x=df_cp[(df_cp[kwargs['legendgroup']] == lgroup) & (df_cp[kwargs['sampleID']] == s)][kwargs['x_name']].values,
    #                     y=df_cp[(df_cp[kwargs['legendgroup']] == lgroup) & (df_cp[kwargs['sampleID']] == s)][kwargs['y_name']].values,
    #                     # mode='markers+lines',
    #                     marker=dict(color=colorsList[i]),
    #                     legendgroup=str(lgroup),
    #                     name=str(lgroup)+'_'+str(s),      
    #                     )
    #             )           
    return cp_sw_fig

# %%
def plot_creation(df, **kwargs):
    # plot_type: 'perm_phi', 'swirr_perm', 'swirr_phi', 'cp_sw', 'ri_sw', 'ff_phi' 
    fileObject = open("layout_templates.json", "r")
    jsonContent = fileObject.read()
    layout_template = json.loads(jsonContent)
    plot=phi_perm_plot(df,**kwargs)
        

    return plot
# %%

if __name__ == '__main__':
    print('Lib with plots')
    try:
        df_1=pd.read_csv(r'data\data.csv', sep=';', header=0, encoding="utf-8")
    except UnicodeDecodeError:
        df_1=pd.read_csv(r'data\data.csv', sep=';', header=0, encoding="cp1251")
    # "cp1251"
# %%
    fig=plot_creation(df_1, 
        x_name='Porosity', 
        y_name='Permeability_Kl',
        x_range=[0,30],
        y_range=[-3,3])
    fig.show()
# %%
