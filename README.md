# ArtiPainter
AI illustrate assistant

<p align="center">
  <br>
  <br>
  <br>
  <span style="font-size:32px;"><strong>Art is a form of communication, the pen and paper will never become obsolete.</strong></span>
  <br>
  <br>
  <br>
</p>


## Instructions

### 1. Installation and Setup
1. Download and install [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).
2. Enable API: Edit `webui-user.bat` and add `--api` to the `set COMMANDLINE_ARGS` line.
3. Download and place the stable diffusion model in `stable-diffusion-webui/models/Stable-diffusion/` folder, then double-click `webui-user.bat` to launch it.
4. Open your browser and go to [http://127.0.0.1:7860/](http://127.0.0.1:7860/) to configure the downloaded model.
5. Download and install Krita from [https://krita.org/](https://krita.org/).
6. Launch Krita and install the ArtiPainter plugin. For instructions on installing Krita plugins, refer to [this link](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin).

### 2. ArtiPainter Usage
1. The plugin consists of three parts:
   1. Input layer group "↓ Input" and output layer "↑ Output": The input layer group sends compositions to stable diffusion for processing based on parameters, and the processing results are returned to the output layer.
   2. ArtiPainter Viewer: Preview the generated image.
   3. Parameter Configuration Panel: Configure stable diffusion parameters, which are consistent with stable-diffusion-webui.
2. After entering the Krita canvas, click "Start Painting" to automatically generate input and output folders.
3. Paint freely, modify parameters until you achieve satisfactory results.
4. Before leaving Krita, click "Stop Painting" to disconnect the link.

### 3. Considerations
1. Confirm that the webui's default URL is [http://127.0.0.1:7860/](http://127.0.0.1:7860/). If not, need manually adjust the settings.
2. Do not connect "Start Painting" without creating a canvas document.
3. Do not paint on the stable diffusion's output layer.
4. Do not delete occupied output layers during link runtime.
5. Do not input symbols other than integers in the seed field, as it may crash.
6. The output layer of stable diffusion and the input layer group are identified by name. Renaming is ok in link enablement, but if names change after restarting the link, new input/output layers/groups will be created.
7. The graphics tablet may experience lag due to compatibility issues with drawing drivers. Separating the tablet driver and Krita onto different CPUs might solve this problem.
8. Efficiency depends on GPU performance. Inputting large-sized images may exceed VRAM capacity.
9. Currently, script execution is not supported. For Lora and Addition Net, please use prompt panel.
10. To change models, manually switch them at [http://127.0.0.1:7860/](http://127.0.0.1:7860/).


# 使用说明

## 1. 安装配置环境
1. 下载并安装 [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
2. 启用API：编辑 `webui-user.bat`，在 `set COMMANDLINE_ARGS` 那一行加入 `--api`
3. 下载并将 stable diffusion 模型放入 `stable-diffusion-webui/models/Stable-diffusion/` 文件夹下，双击 `webui-user.bat` 启动编辑器
4. 使用浏览器打开 [http://127.0.0.1:7860/](http://127.0.0.1:7860/)，配置下载的模型
5. 下载并安装 Krita，Krita 下载地址：[https://krita.org/](https://krita.org/)
6. 启动 Krita 安装 ArtiPainter 插件，Krita 插件使用说明见 [这里](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin)

## 2. ArtiPainter使用说明
1. 软件由三部分构成：
   1. 输入图层组 "↓ Input"，输出图层 “↑ Output”：输入图层组将合成送往 stable diffusion 根据参数进行处理，处理结果返回到输出图层
   2. ArtiPainter Viewer：预览生成图像
   3. 参数配置面板：配置 stable diffusion 参数，所有参数都与 stable-diffusion-webui 一致
2. 进入 Krita 画布后，点击 "Start Painting" 自动生成输入输出文件夹
3. 自由绘画，修改参数，直到得到满意的成果
4. 在离开 Krita 之前，点击 "Stop Painting" 切断链接

## 3. 注意事项
1. 确认 webui 是默认 URL [http://127.0.0.1:7860/](http://127.0.0.1:7860/)，否则需要手动修改设置
2. 不要在没有建立画布的情况下连接 "Start Painting"
3. 不要在 stable diffusion 的输出图层上作画
4. 不要在链接运行时删除占用的输出图层
5. 不要在 seed 栏输入整数以外的符号，会崩溃
6. stable diffusion 的输出图层与输入图层组是按照名称识别的，在链接启用中可以重命名，但重启链接后如果名称已经改变，会新建新的输入输出图层/图层组
7. 数位板有时会卡顿，绘画驱动的兼容性问题，将数位板驱动与 Krita 分隔到不同 CPU 可能会解决这个问题
8. 运行效率取决于显卡性能，大尺寸图像的输入可能会超出显存
9. 当前不支持脚本 script，Lora，Addtion Net 请通过 prompt 面板启用
10. 更改模型需要在 [http://127.0.0.1:7860/](http://127.0.0.1:7860/) 手动切换



## 使用方法

### 1. 環境のインストールと設定
1. [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) をダウンロードしてインストールします。
2. APIを有効にするには、`webui-user.bat` を編集し、`set COMMANDLINE_ARGS` の行に `--api` を追加します。
3. stable diffusion モデルを `stable-diffusion-webui/models/Stable-diffusion/` フォルダに配置し、`webui-user.bat` をダブルクリックしてエディタを起動します。
4. ブラウザで [http://127.0.0.1:7860/](http://127.0.0.1:7860/) を開き、ダウンロードしたモデルを設定します。
5. [Krita](https://krita.org/) をダウンロードしてインストールします。
6. Kritaを起動、ArtiPainterプラグインをインストールします。プラグインの使い方については [こちら](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin) を参照してください。

### 2. ArtiPainterの使い方
1. ソフトウェアは以下の3つの部分で構成されています：
   1. 入力レイヤーグループ "↓ Input"、出力レイヤー "↑ Output"：入力レイヤーグループはパラメータに基づいて stable diffusion に合成され、処理結果が出力レイヤーに返されます。
   2. ArtiPainter Viewer：生成された画像をプレビューします。
   3. パラメータ設定パネル：stable diffusion パラメータを設定します。すべてのパラメータは stable-diffusion-webui と同じです。
2. Kritaのキャンバスに入ったら、"Start Painting" をクリックして入力と出力のフォルダが自動生成されます。
3. 自由に描画し、パラメータを調整、満足のいく結果が得られるまで。
4. Kritaを終了する前に、"Stop Painting" をクリックして接続を切断します。

### 3. 注意事項
1. webui のデフォルトURLが [http://127.0.0.1:7860/](http://127.0.0.1:7860/) であることを確認してください。それ以外の場合は手動で設定を変更する必要があります。
2. キャンバスを作成しない状態で "Start Painting" または "Bklink" に接続しないでください。エラーが発生する可能性があります。
3. stable diffusion の出力レイヤー上で描画しないでください。
4. 接続実行中に使用中の出力レイヤーを削除しないでください。
5. seed欄に整数以外の記号を入力しないでください。クラッシュする可能性があります。
6. stable diffusion の出力レイヤーと入力レイヤーグループは名前によって識別されます。接続が有効な場合、名前を変更できますが、名前が変更されている場合、接続を再起動すると新しい入出力レイヤー/グループが作成されます。
7. ペンタブレットが遅くなることがあります。描画ドライバの互換性の問題です。ペンタブレットドライバとKritaを異なるCPUに分離すると問題が解決する可能性があります。
8. 他のKritaプラグインと互換性の問題があるかもしれません。Ten Brush はKritaをクラッシュさせる可能性があります（低確率）（原因は不明）。
9. 実行効率はGPUの性能に依存し、大きなサイズの画像の入力はVRAMを超える可能性があります。
10. 現在、スクリプトやLora、Addtion Netはサポートされていません。promptパネルを使用してください。
11. モデルを変更するには、[http://127.0.0.1:7860/](http://127.0.0.1:7860/) で手動で切り替える必要があります。

## Credits

- **Stable Diffusion** - [Repository](https://github.com/CompVis/stable-diffusion)
- **stable-diffusion-webui** - [Repository](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- **Krita** - [site](https://krita.org)
- **auto-sd-paint** - [Repository](https://github.com/Interpause/auto-sd-paint-ext)
  - Krita plugin UI
  - config document

## contact information
1. email:narusoracode@gmail.com
2. twitter:[@NRSora5](https://twitter.com/NRSora5)
3. pixiv:[鸣空NRSora](https://www.pixiv.net/users/4855599)

## 支持我的开发：
<img src="https://github.com/NaruSora/document/blob/main/IMG_1.png?raw=true" alt="Wechat Receipt QR code" width="200" height="200">

## supporting developer
1. [on gumroad](https://narusora.gumroad.com/)
2. [on patron](patreon.com/NaruSora)

