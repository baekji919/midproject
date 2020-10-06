data = pd.read_excel("C:/mid_project/top5/Chosun_mer.xlsx", sheet_name='사설pos&neg').dropna().reset_index().drop(
    columns=["index"])

labels = [data['pos'].values, data['neg'].values]
data = [data['pos_value'].values, data['neg_value'].values]
colors = [['#ff9999', '#bbddff', '#99ffbb', '#ffcc99', '#ffb3e6'],
          ['#bbbbbb', '#bbbb99', '#99bbbb', '#778899', '#997799']]
titles = ['조선일보_사설 메르스 긍정어', '조선일보_사설 메르스 부정어']

rcParams.update({'font.size': 10})
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(wspace=0.5)
explode = (0.05, 0, 0, 0, 0)

for i in range(2):
    ax = axes[i]
    ax.pie(data[i], explode=explode, labels=labels[i], colors=colors[i], autopct='%1.1f%%',
           wedgeprops={'linewidth': 3}, pctdistance=0.75, shadow=True, startangle=45)

    #     for w in wedges: # 조각 설정
    #         w.set_linewidth(0)
    #         w.set_edgecolor('w')

    #     for t in texts: # label 설정
    #         t.set_color('k')
    #         t.set_fontsize(12)

    #     for a in autotexts: # 퍼센티지 설정
    #         a.set_color('w')
    #         a.set_fontsize(8)

    centre_circle = plt.Circle((0, 0), 0.60, color='black', fc='white', linewidth=0)
    ax.add_artist(centre_circle)
    #     centre_circle = plt.Circle((0,0),0.60,color='white', fc = 'white', linewidth = 0)
    #     plt.gca().add_artist(centre_circle)

    ax.set_title(titles[i])
    ax.axis('equal')

plt.savefig('ex_pieplot.png', format='png', dpi=300)
plt.show()