android手机给应用分配的内存通常是8兆左右，如果处理内存处理不当很容易造成OutOfMemoryError，我们的产品出现最多的错误也是OutOfMemoryError的异常，  
在解决这个异常时在网上发现很多关于OutOfMemoryError的原因的介绍。  
OutOfMemoryError主要由以下几种情况造成：  
### **1.数据库的cursor没有关闭。**   
操作Sqlite数据库时，Cursor是数据库表中每一行的集合，Cursor提供了很多方法，可以很方便的读取数据库中的值，  
    可以根据索引，列名等获取数据库中的值，通过游标的方式可以调用moveToNext()移到下一行  
    当我们操作完数据库后，一定要记得调用Cursor对象的close()来关闭游标，释放资源。  
### **2.构造adapter没有使用缓存contentview。**  
    在继承BaseAdapter时会让我们重写getView(int position, View   convertView, ViewGroup parent)方法，  
    第二个参数convertView就是我们要用到的重用的对象

Java代码  ![收藏代码](https://www.iteye.com/images/icon_star.png)
```
1.  @Override  
2.  public View getView(int position, View convertView, ViewGroup parent) {  
3.      ViewHolder vHolder = null;  

5.      if (convertView == null) {  
6.          convertView = inflater.inflate(..., null);  

8.          vHolder = new ViewHolder();  
9.          vHolder.img= (ImageView) convertView.findViewById(...);  
10.          vHolder.tv= (TextView) convertView  
11.                  .findViewById(...);  

13.          convertView.setTag(vHolder);  
14.      } else {  

16.          vHolder = (ViewHolder) convertView.getTag();  
17.      }  

19.      vHolder.img.setImageBitmap(...);  
20.      vHolder.tv.setText(...);  
21.      return convertView;  
22.  }  

24.  static class ViewHolder {  
25.      TextView tv;  
26.      ImageView img;  
27.  }  
```
    这里只讲使用方法，具体性能测试文章请见：  
    ListView中getView的原理＋如何在ListView中放置多个item  
    http://www.cnblogs.com/xiaowenji/archive/2010/12/08/1900579.html  
    Android开发之ListView适配器（Adapter）优化  
    http://shinfocom.iteye.com/blog/1231511  
### **3.调用registerReceiver()后未调用unregisterReceiver().**  
     广播接收者（BroadcastReceiver）经常在应用中用到，可以在多线程任务完成后发送广播通知UI更新，也可以接收系统广播实现一些功能  
     可以通过代码的方式注册：  
```
    IntentFilter postFilter = new IntentFilter();  
    postFilter.addAction(getPackageName() + ".background.job");  
    this.registerReceiver(receiver, postFilter);  
```
    当我们Activity中使用了registerReceiver()方法注册了BroadcastReceiver，一定要在Activity的生命周期内调用unregisterReceiver()方法取消注册  
    也就是说registerReceiver()和unregisterReceiver()方法一定要成对出现，通常我们可以重写Activity的onDestory()方法：

Java代码  ![收藏代码](https://www.iteye.com/images/icon_star.png)
```
1.  @Override  
2.  protected void onDestroy() {  
3.        this.unregisterReceiver(receiver);  
4.        super.onDestroy();  
5.  }  
```
### **4.未关闭InputStream/OutputStream。**  
    这个就不多说了，我们操作完输入输出流都要关闭流  
### **5.Bitmap使用后未调用recycle()。**  
    图片处理不好是造成内存溢出的又一个头号原因，（在我们的产品中也有体现)，

    当我们处理完图片之后可以通过调用recycle()方法来回收图片对象

Java代码  ![收藏代码](https://www.iteye.com/images/icon_star.png)
```
1.  if(!bitmap.isRecycled())  
2.  {  
3.      bitmap.recycle()  
4.  }          
```
    除此之外：  
    直接使用ImageView显示bitmap会占用较多资源，特别是图片较大的时候，可能导致崩溃。  
    使用BitmapFactory.Options设置inSampleSize, 这样做可以减少对系统资源的要求。  
    属性值inSampleSize表示缩略图大小为原始图片大小的几分之一，即如果这个值为2，则取出的缩略图的宽和高都是原始图片的1/2，图片大小就为原始大小的1/4。  
```
        BitmapFactory.Options bitmapFactoryOptions = new BitmapFactory.Options();   
        bitmapFactoryOptions.inJustDecodeBounds = true;   
        bitmapFactoryOptions.inSampleSize = 2;   
        // 这里一定要将其设置回false，因为之前我们将其设置成了true   
        // 
```

设置inJustDecodeBounds为true后，decodeFile并不分配空间，即，BitmapFactory解码出来的Bitmap为Null,但可计算出原始图片的长度和宽度   
```
        options.inJustDecodeBounds = false;  
        Bitmap bmp = BitmapFactory.decodeFile(sourceBitmap, options);   
```
### **6.Context泄漏。**  
    这是一个很隐晦的OutOfMemoryError的情况。先看一个Android官网提供的例子：

Java代码  ![收藏代码](https://www.iteye.com/images/icon_star.png)
```
1.  private static Drawable sBackground;  
2.  @Override  
3.  protected void onCreate(Bundle state) {  
4.    super.onCreate(state);  

6.    TextView label = new TextView(this);  
7.    label.setText("Leaks are bad");  

9.    if (sBackground == null) {  
10.      sBackground = getDrawable(R.drawable.large\_bitmap);  
11.    }  
12.    label.setBackgroundDrawable(sBackground);  

14.    setContentView(label);  
15.  }  
```
    这段代码效率很快，但同时又是极其错误的；  
    在第一次屏幕方向切换时它泄露了一开始创建的Activity。当一个Drawable附加到一个 View上时，  
    View会将其作为一个callback设定到Drawable上。上述的代码片段，意味着Drawable拥有一个TextView的引用，  
    而TextView又拥有Activity（Context类型）的引用，换句话说，Drawable拥有了更多的对象引用。即使Activity被 销毁，内存仍然不会被释放。  
    另外，对Context的引用超过它本身的生命周期，也会导致Context泄漏。所以尽量使用Application这种Context类型。  
    这种Context拥有和应用程序一样长的生命周期，并且不依赖Activity的生命周期。如果你打算保存一个长时间的对象，  
    并且其需要一个 Context，记得使用Application对象。你可以通过调用Context.getApplicationContext()或 Activity.getApplication()轻松得到Application对象。  
    最近遇到一种情况引起了Context泄漏，就是在Activity销毁时，里面有其他线程没有停。  
    总结一下避免Context泄漏应该注意的问题：  
    1.使用Application这种Context类型。  
    2.注意对Context的引用不要超过它本身的生命周期。  
    3.慎重的使用“static”关键字。  
    4.Context里如果有线程，一定要在onDestroy()里及时停掉。  
### **7.static关键字**  
    当类的成员变量声明成static后，它是属于类的而不是属于对象的，如果我们将很大的资源对象（Bitmap，context等）声明成static，那么这些资源不会随着对象的回收而回收，  
    会一直存在，所以在使用static关键字定义成员变量的时候要慎重。
