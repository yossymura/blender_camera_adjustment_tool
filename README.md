# blender_camera_adjustment_tool

Blenderで簡易的なカメラ操作するためのアドオンの試作。  
3Dビュー上でマウス操作により角度や向きなどを簡単に調整できる。

![camera_adjustment](https://user-images.githubusercontent.com/42290408/106368174-04f98f00-638b-11eb-9c8f-dc7908c53c11.jpg)
 
# Features
 
- カメラ選択：カメラの選択、カメラビューのON/OFF
- 手動調整：角度、位置、回転、ズームを、マウス操作で直接調整
- 一定間隔で調整：指定した角度や距離単位にボタンで調整
- ターゲットへ向ける：指定したターゲットに各方向からカメラを向ける

※「ターゲットへ向ける」機能はコンストレイントが設定されていないカメラで利用可
 
# Requirement

Blender2.8 以降で動作する想定。  
Blender2.91.0 で動作確認済み。
 
# Installation

1. zipをダウンロードして解凍
![download](https://user-images.githubusercontent.com/42290408/106333848-d87f3d80-62cc-11eb-845c-cea4d2b50ee4.jpg)
1. Blenderのプリファレンス → アドオン → インストール からcamera_adjustment_tool.py をインストール後、有効化する。
