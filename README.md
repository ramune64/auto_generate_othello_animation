<h1>オセロのアニメーションを対局のデータに基づいて自動で生成できるもの</h1>
<p>動作確認:blender4.3</p>
<p>近日公開予定のe_coach_AIというソフトの「振り返りモード」を利用して、各手の記録と点数が記録された.pklファイルが生成されます。(pkls/full_{動画名}.pkl)これを利用してアニメーションの構成を自動で生成できます。</p>
<h2>使い方</h2>
<ul>
  <li>1.e-coach_AIの「振り返りモード」を用いて、.pklファイルを生成する。</li>
  <li>2.「オセロ.blend」を開く。</li>
  <li>3.スクリプト作成を開き、script_all.pyを読み込む。</li>
  <li>4.「ウィンドウ」から、「システムコンソール切り替え」を押し、コンソール画面を開く。</li>
  <li>5.blenderの画面からスクリプトを実行。</li>
  <li>6.コンソールで、pklファイルのパスを聞かれるので入力。</li>
  <li>7.実行が終わるのを待つと、棋譜と同じゲーム展開のアニメーションが作られる。</li>
  <li>8.あとはレンダリングするだけ。</li>
</ul>
<p>サンプルの.pklファイルが付属しています。また、その実行結果をレンダリングしたものは<a href="https://drive.google.com/file/d/1ddNBA8maDiZ6IqaNGkEJAkDuN06m5FVy/view?usp=sharing" target="_blank" rel="noopener noreferrer">こちら</a>からご覧いただけます。</p>
<img src="image.png">
<img src="image2.png">
