import os
import tarfile
from six.moves import urllib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
import matplotlib.image as mping
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelBinarizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array
from sklearn.preprocessing import LabelEncoder
from scipy import sparse
#设置pandas打印省略号的问题
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets","housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()
# 加载数据
def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path,"housing.csv")
    return pd.read_csv(csv_path) # 返回一个包含所有数据的Pandas DataFrame 对象

#创建测试集（20%）
def split_train_test(data, test_ratio):
    #设置随机数生成器种子
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    print(shuffled_indices)
    return data.iloc[train_indices], data.iloc[test_indices]

#判断实例是否应该放入测试集
def test_set_check(identifier, test_ratio, hash):
    return hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio

def split_train_test_by_id(data, test_ratio, id_column, hash=hashlib.md5):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio, hash))
    return data.loc[~in_test_set], data.loc[in_test_set]

# 对比总数据集、分层采样的测试集、纯随机采样测试集的收入分类比例。
def income_cat_proportions(data):
    return data['income_cat'].value_counts() / len(data)


if __name__ == "__main__":
    #创建datasets/housing目录
    #fetch_housing_data()

    #加载数据
    housing = load_housing_data()

    # 查看前5行数据
    #print(housing.head(n=5))

    #查看数据信息
    # housing.info()

    #print(housing.describe())

    #绘制柱状图
    #housing.hist(bins=50,figsize=(20, 15))
    #plt.show()

    #创建测试集（该方法的缺陷是多次运行之后会得到整个数据集）
    # train_set, test_set = split_train_test(housing, 0.2)
    # print(len(train_set), "train +", len(test_set), "test")

    #使用行索引作为id
    # housing_with_id = housing.reset_index() # add an 'index' column
    # train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, 'index')

    #用最稳定的特征来创建唯一识别码
    # housing_with_id["id"] = housing["longitude"] * 1000 + housing["latitude"]
    # train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "id")

    # 使用sklearn提供的函数分割数据集
    # train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
    # print(test_set.head())

    #收入分配柱状图
    housing['median_income'].hist()
    # plt.show()

    #创建收入类别属性，产生离散的分类
    # 收入中位数除以1.5以限制收入分类的数量
    housing['income_cat'] = np.ceil(housing['median_income'] / 1.5)
    # Label those above 5 as 5
    housing['income_cat'].where(housing['income_cat'] < 5, 5.0, inplace=True)

    # 查看收入分类的比例
    print(housing['income_cat'].value_counts() / len(housing))

    # 处理后的收入分配柱状图
    housing['income_cat'].hist()
    # plt.show()

    # 根据收入分类，进行分层采样
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(housing, housing['income_cat']):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]

    # 查看收入分类的比例
    print(strat_test_set['income_cat'].value_counts() / len(strat_test_set))

    train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

    # 对比总数据集、分层采样的测试集、纯随机采样测试集的收入分类比例。
    compare_props = pd.DataFrame({
        "Overall": income_cat_proportions(housing),
        "Stratified": income_cat_proportions(strat_test_set),
        "Random": income_cat_proportions(test_set)
    }).sort_index()

    compare_props["Rand. %error"] = 100 * compare_props["Random"] / compare_props["Overall"] - 100
    compare_props["Strat. %error"] = 100 * compare_props["Stratified"] / compare_props["Overall"] - 100
    print(compare_props)

    # 删除income_cat 属性，使数据回到初始状态
    for set_ in (strat_train_set, strat_test_set):
        set_.drop(['income_cat'], axis=1, inplace=True)

    # 创建训练集副本，以免损伤训练集
    housing = strat_train_set.copy()

    # 地理数据可视化
    housing.plot(kind='scatter', x='longitude', y='latitude')
    # 先保存再显示
    # plt.savefig('bad_visualization_plot')
    # plt.show()

    # 显示高密度区域散点图
    housing.plot(kind='scatter', x='longitude', y='latitude', alpha=0.1)
    # plt.savefig('better_visualization_plot')

    # 加州房价
    housing.plot(kind='scatter', x='longitude', y='latitude', alpha=0.4,
                 s=housing['population'] / 100, label='population', figsize=(10, 7),
                 c='median_house_value', cmap=plt.get_cmap('jet'), colorbar=True,
                 )
    plt.legend()
    # plt.savefig('housing_price_scatterplot')
    # plt.show()

    #加入地图背景
    # Ubuntu 系统
    # california_img = mping.imread('/home/xyk/anaconda3/envs/ML_sklearn_tf/ML-机器学习/2、机器学习项目实例' +'/images/end_to_end_project/california.png')
    # windows 系统
    california_img = mping.imread('C:\File\Algorithm-Interview-And-Written-Summary\_codes\machine_learning\一个完整的机器学习项目实例' +'/images/end_to_end_project/california.png')

    ax = housing.plot(kind='scatter', x='longitude', y='latitude', alpha=0.4,
                 s=housing['population'] / 100, label='population', figsize=(10, 7),
                 c='median_house_value', cmap=plt.get_cmap('jet'), colorbar=False,)
    plt.imshow(california_img, extent=[-124.55, -113.80, 32.45, 42.05], alpha=0.5,
               cmap=plt.get_cmap('jet'))
    plt.ylabel('Latitude', fontsize=14)
    plt.xlabel("Longitude", fontsize=14)

    prices = housing["median_house_value"]
    tick_values = np.linspace(prices.min(), prices.max(), 11)
    cbar = plt.colorbar()
    cbar.ax.set_yticklabels(["$%dk" % (round(v / 1000)) for v in tick_values], fontsize=14)
    cbar.set_label('Median House Value', fontsize=16)

    plt.legend(fontsize=16)
    # plt.savefig("california_housing_prices_plot")
    # plt.show()

    # 每个属性和房价中位数的关联度
    # corr_matrix = housing.corr()
    # 打印关联度
    # print(corr_matrix['median_house_value'].sort_values(ascending=False))

    # 画出每个数值属性对每个其他数值属性的图
    attributes = ['median_house_value','median_income','total_rooms','housing_median_age']
    scatter_matrix(housing[attributes],figsize=(12, 8))
    plt.savefig('scatter_matrix_plot')
    # plt.show()

    # 将最有希望用来预测房价中位数的属性是收入中位数，放大
    housing.plot(kind='scatter', x='median_income', y='median_house_value', alpha=0.1)
    # plt.show()

    #尝试新的属性组合
    housing['rooms_per_household'] = housing['total_rooms']/housing['households']
    housing['bedrooms_per_room'] = housing['total_bedrooms']/housing['total_rooms']
    housing['population_per_household'] = housing['population']/housing['households']
    # 查看相关矩阵
    corr_matrix = housing.corr()
    print(corr_matrix['median_house_value'].sort_values(ascending=False))

#为机器学习算法准备数据‘
    print('描述数据',housing.describe())
    # 备份数据
    housing = strat_train_set.drop('median_house_value', axis=1)
    housing_labels = strat_train_set['median_house_value'].copy()

    # 数据清洗
    sample_incomplete_rows = housing[housing.isnull().any(axis=1)].head()
    print(sample_incomplete_rows)

    # sample_incomplete_rows.dropna(subset=['total_bedrooms']) # 方案一：去掉对应的街区
    # sample_incomplete_rooms.drop('total_bedrooms',axis=1) # 方案二：去掉整个属性
    median = housing['total_bedrooms'].median()
    sample_incomplete_rows['total_bedrooms'].fillna(median, inplace=True) # 方案三：进行赋值
    print(sample_incomplete_rows)

    # 创建Imputer属性，指定用某属性的中位数来替代该属性所有的缺失值
    imputer = Imputer(strategy='median')

    # 创建一份没有文本属性的数据副本
    housing_num = housing.drop('ocean_proximity', axis=1)
    # 将imputer实例拟合到训练数据
    imputer.fit(housing_num)

    #imputer计算出每个属性的中位数，并将结果存在实例变量statistics_中，将imputer应用到每个数值
    print('中位数：', imputer.statistics_)
    print(housing_num.median().values)

    # 使用上面的imputer对训练集进行转换，将缺失值替换为中位数
    X = imputer.transform(housing_num)
    #将其放回到DataFrame中
    housing_tr = pd.DataFrame(X, columns=housing_num.columns,index=list(housing.index.values))
    print(housing_tr.loc[sample_incomplete_rows.index.values])
    # print('housing_tr:',housing_tr)
    print(imputer.strategy)

    housing_tr = pd.DataFrame(X, columns=housing_num.columns)
    print(housing_tr.head())

    # Now let's preprocess the categorical input feature, ocean_proximity:
    housing_cat = housing[['ocean_proximity']]
    print(housing_cat.head())

    # 这些文本标签转换为数字
    ordinal_encoder = OrdinalEncoder()
    housing_cat_encoded = ordinal_encoder.fit_transform(housing_cat)
    # print(housing_cat_encoded[:10])

    # print(ordinal_encoder.categories_)

    # 将整数分类值转变为独热向量
    # encoder = OneHotEncoder()
    # housing_cat_1hot = encoder.fit_transform(housing_cat_encoded.reshape(-1, 1))
    # print(housing_cat_1hot)

    # 将其转换为密集矩阵
    # print('密集矩阵：',housing_cat_1hot.toarray())

    # 使用类LabelBinarizer 可以执行两个转换（从文本分类到整数分类，再从整数分类到独热向量
    # 传入参数 sparse_output=True 可得到一个稀疏矩阵
    encoder = LabelBinarizer(sparse_output=True)
    # housing_cat_1hot = encoder.fit_transform(housing_cat)
    # print(housing_cat_1hot)

    # 使用sklearn提供的CategoricalEncoder类(将来可用)
    from sklearn.preprocessing import CategoricalEncoder

    # cat_encoder = CategoricalEncoder()
    # housing_cat_reshaped = housing_cat.values.reshape(-1, 1)
    # housing_cat_1hot = cat_encoder.fit_transform(housing_cat_reshaped)



