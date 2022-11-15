### 一、环境配置 

Google官方文档： [https://source.android.com/setup/build/downloading](https://source.android.com/setup/build/downloading ) 


安装Repo： 


```
mkdir ~/bin 
PATH=~/bin:$PATH
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```

初始化repo： 

```
mkdir WORKING_DIRECTORY 
cd WORKING_DIRECTORY
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

 从这个链接 [https://source.android.com/setup/start/build-numbers#source-code-tags-and-builds](https://source.android.com/setup/start/build-numbers#source-code-tags-and-builds) 获取一个分支地址，使用``repo init``进行初始化。当前最新的tag分支为``android-10.0.0_r20``，如下图。我们下载此分支: 


![](http://i.vjob.top:8000/imgs/vjob_tags-300x159.png)

### 二、执行下载：



```
repo init --depth 1 -u https://android.googlesource.com/platform/manifest -b android-10.0.0_r20
repo sync -c -j4
```

### 三、下载LineageOS-17.1


参考[https://wiki.lineageos.org/devices/bacon/build](https://wiki.lineageos.org/devices/bacon/build)：

```
mkdir Lineage-17.1/
cd Lineage-17.1/
repo init -u https://github.com/LineageOS/android.git -b lineage-17.1
repo sync -c -j8
```


原文链接： [http://droid10.com/2019/12/30/1、android10源码下载/]( http://droid10.com/2019/12/30/1、android10源码下载/)
