# NASA-TLX

## 概要
NASA-TLXに基づいてユーザーの作業負荷を評価するためのアンケートツールです．

参考：[NASA-TLX](https://www.jstage.jst.go.jp/article/jje/51/6/51_391/_pdf)

## 機能
- 一対比較の結果を"【被験者名】_compare.csv"に出力
- 作業負荷の結果(スライダーの数値)と算出したワークロードスコアを"【被験者名】_result.csv"に出力

## ダウンロード
ページ右側の"Releases"から実行ファイルをダウンロードするか，[こちら](https://github.com/chansei/nasa_tlx/releases/tag/v1.1)からダウンロードページにアクセスしてください．

## 使い方
1. 【実験者】被験者名とタスク数を入力します．
1. 【被験者】(初回タスク後のみ)一対比較方式を使用して2つの尺度を比較します．
1. 【被験者】各尺度のスライダーを使用して，作業負荷の具体的な評価を行います．

## 動作要件
- Windows 10 x64 / 11 x64
- 画面サイズが1920x1080であること(これ以外の解像度でも動作はしますが表示が崩れる可能性があります)

## 特記事項
- 実行ファイルがWindows Defender等にて"悪意のあるファイル"と判定されることがあります([virustotal](https://www.virustotal.com/gui/file/27960a86d05f41c139d27bf9c1cba0f50acd745ec7a23e4e4709055f39403ea1/detection))．  
必要に応じてブロックを解除して実行する，元のpythonスクリプトをコンパイルする等の対応をしてください．

## 更新履歴
### 1.0(23/10/30)
- プログラム作成
### 1.1(23/10/31)
- アイコン追加
