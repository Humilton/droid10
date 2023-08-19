### 一、环境配置 

##### Google官方文档： [https://source.android.com/setup/build/downloading](https://source.android.com/setup/build/downloading ) 


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


![](https://img.vjob.top/imgs/vjob_tags-300x159.png)


同步android-10.0.0_r20代码：
```
repo init --depth 1 -u https://android.googlesource.com/platform/manifest -b android-10.0.0_r20
repo sync -c -j4
```

##### 中国科学技术大学开源软件镜像 : <https://mirrors.ustc.edu.cn/help/aosp.html>
在~/.bashrc中配置repo
```
export REPO_URL='https://gerrit-googlesource.proxy.ustclug.org/git-repo'
```

同步android-security-10.0.0_r66代码：
```
mkdir android10-security-release && cd android10-security-release
repo init --depth 1 -u git://mirrors.ustc.edu.cn/aosp/platform/manifest -b android-security-10.0.0_r66
repo sync -c -j4
```

同步android-12.1.0_r5代码：
```
mkdir android-12.1.0 && cd android-12.1.0
repo init --depth 1 -u git://mirrors.ustc.edu.cn/aosp/platform/manifest -b android-12.1.0_r5
repo sync -c -j4
```

压缩分享：
```
tar --exclude=".*" --exclude="out" -cvf android10-security-release.tar.gz android10-security-release
tar --exclude=".*" --exclude="out" -cvf android-12.1.0.tar.gz android-12.1.0
```

##### 清华源 :　<https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/>

同步android-security-10.0.0_r66代码：
```
mkdir android10-security-release && cd android10-security-release
repo init --depth 1 -u https://mirrors.tuna.tsinghua.edu.cn/git/AOSP/platform/manifest -b android-security-10.0.0_r66
repo sync -c -j4
```

同步android-12.1.0_r5代码：
```
mkdir android-12.1.0 && cd android-12.1.0
repo init --depth 1 -u https://mirrors.tuna.tsinghua.edu.cn/git/AOSP/platform/manifest -b android-12.1.0_r5
repo sync -c -j4
```


### 二、下载LineageOS-17.1


参考[https://wiki.lineageos.org/devices/bacon/build](https://wiki.lineageos.org/devices/bacon/build)：

```
mkdir Lineage-17.1/
cd Lineage-17.1/
repo init -u https://github.com/LineageOS/android.git -b lineage-17.1
repo sync -c -j8
```

