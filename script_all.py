import bpy
import numpy as np
import pickle
from math import radians
import sys
import os

# .blendファイルがある場所を基準にする
base_path = bpy.path.abspath("//")  # "//" はblendファイルのディレクトリを表す
module_path = os.path.join(base_path, "modules")

if module_path not in sys.path:
    sys.path.append(module_path)

import othello_play
x = {
    "4":0.12,
    "5":-0.12
}
y = {
    "d":0.12,
    "e":-0.12
}
def str2pos(action:str) -> tuple:
    action_col = action[0]
    action_col_ascii = ord(action_col)
    diff_col = d_ascii - action_col_ascii
    y_pos = 0.12 + diff_col*0.24
    action_row = int(action[1])
    diff_row = 4 - action_row
    x_pos = 0.12 + diff_row*0.24
    action_pos = (x_pos,y_pos)
    return action_pos
text_settings = {}
previous_frame = -1  # 直前のフレームを記録
def update_text(scene):
    current_frame = scene.frame_current
    global previous_frame
    if current_frame != previous_frame:
        previous_frame = current_frame  # フレームを更新
        for obj_name in text_settings:
            #text_obj = bpy.data.objects.get(obj_name)
            text_obj = bpy.data.objects[obj_name]
            settings = text_settings[obj_name]
            for setting in settings:
                if setting[0] <= current_frame and setting[1] >= current_frame:
                    text_obj.data.body = setting[2]
                    if len(setting[2]) == 5:
                        text_obj.scale = (0.145,0.145,0.145)
                    elif len(setting[2]) == 6:
                        text_obj.scale = (0.125,0.125,0.125)
                    else:
                        text_obj.scale = (0.188,0.188,0.188)
                    xpos,ypos = str2pos(obj_name[-2:])
                    text_obj.location = (xpos, ypos-0.02, text_obj.location.z)  # 必要な座標に変更
                    if current_frame == setting[0] or current_frame-1 == setting[1]:
                        #if not text_obj.animation_data or not text_obj.animation_data.action:
                            text_obj.keyframe_insert(data_path="location", frame=current_frame)
                            text_obj.keyframe_insert(data_path="scale", frame=current_frame)
                    #bpy.context.view_layer.update()  # 変更を反映
                    text_obj.data.offset_x = 0
                    text_obj.data.offset_y = 0
                    #bbox = text_obj.bound_box  # 境界ボックスを取得
                    #min_x = min(v[0] for v in bbox)
                    #max_x = max(v[0] for v in bbox)
                    #min_y = min(v[1] for v in bbox)
                    #max_y = max(v[1] for v in bbox)
                    #scale_x, scale_y = text_obj.scale.x, text_obj.scale.y
                    #center_x = (min_x + max_x) / 2 * scale_x
                    #center_y = (min_y + max_y) / 2 * scale_y
                    
                    """ width = text_obj.dimensions.x
                    height = text_obj.dimensions.y
                    center_x,center_y = width/2,height/2 """
                    
                    #text_obj.location.x = xpos
                    #text_obj.location.y = ypos
                    # 原点を中央に維持するために位置を調整
                    
                    #text_obj.location.x -= center_x
                    #text_obj.location.y -= center_y+0.02
                    #print(f"dimensions: {text_obj.dimensions}")
                    #print(f"align_x: {text_obj.data.align_x}, align_y: {text_obj.data.align_y}")
                    #print(obj_name[4],obj_name[-2:],":",xpos,ypos,":",text_obj.location.x,text_obj.location.y)

f_name = "full_test4.pkl"
def remove_all_keyframes():
    target_keywords = ["target", "stone", "テキスト"]  # オブジェクト名に含まれるキーワード
    origin_list = ["target1_c3","target2_b6","テキスト1_c3","テキスト2_c5","stone_d4","stone_d5","stone_e4","stone_e5"]
    for obj in bpy.data.objects:
        if any(keyword in obj.name for keyword in target_keywords):  # 指定ワードを含むオブジェクトか
            # **オブジェクトのキーフレーム削除**
            if obj.animation_data and obj.animation_data.action:
                obj.animation_data.action.fcurves.clear()
                print(f"Removed keyframes from object: {obj.name}")

            # **マテリアルのアニメーション削除**
            for slot in obj.material_slots:
                mat = slot.material
                if mat and mat.use_nodes and mat.node_tree:
                    if mat.animation_data and mat.animation_data.action:
                        mat.animation_data.action.fcurves.clear()
                        print(f"Removed keyframes from material: {mat.name}")

                    # **ノードツリーを検索**
                    for node in mat.node_tree.nodes:
                        if isinstance(node, bpy.types.ShaderNodeBsdfPrincipled):  # BSDFノード
                            alpha_input = node.inputs.get("Alpha")
                            if alpha_input:
                                try:
                                    alpha_input.keyframe_delete("default_value")  # キーフレーム削除
                                    alpha_input.default_value = 1.0  # Alphaを1.0に設定
                                    print(f"Set Alpha to 1 in {mat.name}")
                                except RuntimeError:
                                    print(f"Failed to delete Alpha keyframe in {mat.name}")

                        if isinstance(node, bpy.types.ShaderNodeEmission):  # 放射ノード
                            strength_input = node.inputs.get("Strength")
                            if strength_input:
                                try:
                                    strength_input.keyframe_delete("default_value")  # キーフレーム削除
                                    if "テキスト" in obj.name:
                                        strength_input.default_value = 30  # 「テキスト」の場合、放射強度を30
                                        print(f"Set Emission Strength to 30 in {mat.name}")
                                    else:
                                        print(f"Removed Emission Strength keyframe in {mat.name}")
                                except RuntimeError:
                                    print(f"Failed to delete Emission Strength keyframe in {mat.name}")
            if not obj.name in origin_list:
                bpy.data.objects.remove(obj,do_unlink=True)



with open(f_name, 'rb') as f:
    data = pickle.load(f)
#print(data)
b = np.array([#初期の盤面を表す配列
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1,-1, 0, 0, 0],
    [0, 0, 0,-1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
    ])
white = othello_play.board_to_bitboard(b.copy(), 1)&0xFFFFFFFFFFFFFFFF
black = othello_play.board_to_bitboard(b.copy(), -1)&0xFFFFFFFFFFFFFFFF
next_board = [white,black]
#record = "e6d6c6f4c3c4e3d7c7f6d3c5c8f3f5f7b6b5e7f8g5a6b4e8f2a3g6b3d8b8a5a4b2h6b7a1h7g4h4h5b1a2c2a8a7c1d2h8g7e1d1g8f1e2g2h3g3g1h1h2"
active = bpy.data.objects["テキスト1_a2"]
if active and active.type == 'FONT':
    active_font = active.data.font
    for obj in bpy.context.selected_objects:
        if obj.type == 'FONT' and obj != active:
            obj.data.font = active_font
            print(f"{obj.name} にフォントをコピーしました。")
else:
    print("アクティブなテキストオブジェクトが必要です。")
record = data[0]["record"]
next_color = -1
d_ascii = ord("d")
print("start")
next_start_F = 300
remove_all_keyframes()

for turn_num in range(1,len(record)//2+1):
    color = next_color
    current_board = next_board
    action = record[(turn_num-1)*2:(turn_num-1)*2+2]
    print(color)
    print("turn:",turn_num)
    print(action)
    pl_color_str = "white" if color == 1 else "black"
    next_board = [0,0]
    next_board[0],next_board[1],flips = othello_play.identify_flip_stone(pl_color_str,current_board[0],current_board[1],action,mode=2)
    next_pl_color_str = "white" if color == -1 else "black"
    next_legal = othello_play.get_legal_square(next_pl_color_str,next_board[0],next_board[1])
    if len(next_legal) == 0:#次の盤面で、相手の置ける場所が無いなら
        next_color = color#もう一度同じ色のターン
    else:
        next_color = color*-1
    #if turn_num != 4 and turn_num != 5 and turn_num != 6 and turn_num != 7 and turn_num != 8 and turn_num != 9 and turn_num != 10:
    if turn_num > 60:
        continue
    #ここより下にblender内での処理を記述
    action_pos = str2pos(action)
    print(action_pos)
    legals = othello_play.get_legal_square(pl_color_str,current_board[0],current_board[1])
    print(legals)
    scores = data[turn_num]["scores"]
    for legal in legals:
        legal_str = othello_play.convert_act_bit2str(legal)
        print("legal:",legal_str)
        legal_pos = str2pos(legal_str)
        print(legal_pos)
        if color == 1:
            target_obj_name = "target2_"+legal_str
        else:
            target_obj_name = "target1_"+legal_str
        try:
            target_obj = bpy.data.objects[target_obj_name]
        except KeyError:
            if color == -1:
                original = bpy.data.objects["target1_c3"]
                new_name = "target1_"+legal_str
            else:
                original = bpy.data.objects["target2_b6"]
                new_name = "target2_"+legal_str
            target_obj = original.copy()
            target_obj.name = new_name
            target_obj.data = original.data.copy()  # メッシュデータも複製する
            # シーンに追加
            bpy.context.collection.objects.link(target_obj)
            # マテリアルを独立させる
            if original.data.materials:
                new_materials = [mat.copy() for mat in original.data.materials]  # マテリアルをコピー
                target_obj.data.materials.clear()  # 既存のマテリアルスロットを削除
                for mat in new_materials:
                    target_obj.data.materials.append(mat)  # 新しいマテリアルを追加
            # キーフレームを削除
            if target_obj.animation_data and target_obj.animation_data.action:
                target_obj.animation_data.action = target_obj.animation_data.action.copy()  # 新しいアクションを作成
                target_obj.animation_data.action.fcurves.clear()  # 全キーフレーム削除
            bpy.context.scene.frame_set(next_start_F)
            target_obj.location = (legal_pos[0],legal_pos[1],1.94965)
        bpy.context.scene.frame_set(next_start_F-1)
        target_obj.hide_render = True  # レンダリング時に非表示
        #target_obj.hide_viewport = True
        target_obj.keyframe_insert("hide_render")
        #target_obj.keyframe_insert("hide_viewport")
        bpy.context.scene.frame_set(next_start_F)
        mat = target_obj.active_material  # オブジェクトのアクティブマテリアルを取得
        node = mat.node_tree.nodes["放射"]
        emission_strength = node.inputs["Strength"]  # 放射の強さを取得
        emission_strength.default_value = 1.5
        emission_strength.keyframe_insert("default_value")
        target_obj.hide_render = False  # レンダリング時に表示
        last_hide = False
        #target_obj.hide_viewport = False
        target_obj.keyframe_insert("hide_render")
        #target_obj.keyframe_insert("hide_viewport")
        bpy.context.scene.frame_set(next_start_F+20)
        emission_strength.default_value = 15
        emission_strength.keyframe_insert("default_value")
        timings = [26,29,32,35,38]
        for timing in timings:
            bpy.context.scene.frame_set(next_start_F+timing)
            target_obj.hide_render = not last_hide  # レンダリング時に非表示
            last_hide = not last_hide
            #target_obj.hide_viewport = not target_obj.hide_viewport
            target_obj.keyframe_insert("hide_render")
            #target_obj.keyframe_insert("hide_viewport")
        if legal_str == action:
            bpy.context.scene.frame_set(next_start_F+90)
            mat = target_obj.active_material  # オブジェクトのアクティブマテリアルを取得
            node = mat.node_tree.nodes["放射"]  # 「Emission」ノードを取得
            emission_strength = node.inputs["Strength"]  # 放射の強さを取得
            emission_strength.default_value = 1.5
            emission_strength.keyframe_insert("default_value")
            target_obj.hide_render = False  # レンダリング時に表示
            #target_obj.hide_viewport = False
            target_obj.keyframe_insert("hide_render")
            #target_obj.keyframe_insert("hide_viewport")
            bpy.context.scene.frame_set(next_start_F+105)
            emission_strength.default_value = 30
            emission_strength.keyframe_insert("default_value")
            bpy.context.scene.frame_set(next_start_F+110)
            emission_strength.default_value = 15
            emission_strength.keyframe_insert("default_value")
            bpy.context.scene.frame_set(next_start_F+140)
            emission_strength.default_value = 15
            emission_strength.keyframe_insert("default_value")
            bpy.context.scene.frame_set(next_start_F+153)
            emission_strength.default_value = 1.5
            emission_strength.keyframe_insert("default_value")
            target_obj.hide_render = True  # レンダリング時に非表示
            #target_obj.hide_viewport = True
            target_obj.keyframe_insert("hide_render")
    
            #target_obj.keyframe_insert("hide_viewport")
        
        #print(score)
        if color == 1:
            score_obj_name = "テキスト2_"+legal_str
        else:
            score_obj_name = "テキスト1_"+legal_str
        try:
            score_obj = bpy.data.objects[score_obj_name]
        except KeyError:
            if color == -1:
                original = bpy.data.objects["テキスト1_c3"]
                new_name = "テキスト1_"+legal_str
            else:
                original = bpy.data.objects["テキスト2_c5"]
                new_name = "テキスト2_"+legal_str
            score_obj = original.copy()
            score_obj.name = new_name
            score_obj.data = original.data.copy()  # メッシュデータも複製する
            # シーンに追加
            bpy.context.collection.objects.link(score_obj)
            # マテリアルを独立させる
            if original.data.materials:
                new_materials = [mat.copy() for mat in original.data.materials]  # マテリアルをコピー
                score_obj.data.materials.clear()  # 既存のマテリアルスロットを削除
                for mat in new_materials:
                    score_obj.data.materials.append(mat)  # 新しいマテリアルを追加
            # キーフレームを削除
            if score_obj.animation_data and score_obj.animation_data.action:
                score_obj.animation_data.action = score_obj.animation_data.action.copy()  # 新しいアクションを作成
                score_obj.animation_data.action.fcurves.clear()  # 全キーフレーム削除
            text_settings[new_name] = []
            score_obj_name = new_name
        if not score_obj_name in text_settings:
                text_settings[score_obj_name] = []
        #score_obj.location = (legal_pos[0],legal_pos[1],score_obj.location[2])
        score_obj.data.align_x = 'CENTER'
        score_obj.data.align_y = 'CENTER'
        bpy.context.scene.frame_set(next_start_F+36)
        score_obj.hide_render = True  # レンダリング時に非表示
        score_obj.keyframe_insert("hide_render")
        bpy.context.scene.frame_set(next_start_F+37)
        score_obj.hide_render = False  # レンダリング時に表示
        score_obj.keyframe_insert("hide_render")
        bpy.context.scene.frame_set(next_start_F+90)
        score_obj.hide_render = True  # レンダリング時に非表示
        score_obj.keyframe_insert("hide_render")
    next_start_F2 = next_start_F + 153 + 30
    for legal in legals:
        legal_str = othello_play.convert_act_bit2str(legal)
        if color == 1:
            score_obj_name = "テキスト2_"+legal_str
        else:
            score_obj_name = "テキスト1_"+legal_str
        score = scores[legal_str]
        score = round(score*10)/10
        text_settings[score_obj_name].append((next_start_F,next_start_F2-1,str(score)))
    stone_obj_name = "stone_"+action
    try:
        stone_obj = bpy.data.objects[stone_obj_name]
    except KeyError:
        original = bpy.data.objects["stone_d4"]
        stone_obj = original.copy()
        stone_obj.name = stone_obj_name
        stone_obj.data = original.data.copy()  # メッシュデータも複製する
        # シーンに追加
        bpy.context.collection.objects.link(stone_obj)
        
        # キーフレームを削除
        if stone_obj.animation_data and stone_obj.animation_data.action:
            stone_obj.animation_data.action = stone_obj.animation_data.action.copy()  # 新しいアクションを作成
            stone_obj.animation_data.action.fcurves.clear()  # 全キーフレーム削除
    bpy.context.scene.frame_set(next_start_F+120)
    stone_obj.hide_render = True
    stone_obj.keyframe_insert("hide_render")
    bpy.context.scene.frame_set(next_start_F+121)
    stone_obj.hide_render = False
    stone_obj.keyframe_insert("hide_render")
    if color == 1:
        stone_obj.rotation_euler = (radians(0),radians(0),radians(0))
        stone_obj.location = (action_pos[0],action_pos[1],0.8)
        rotate_y = 0
    else:
        stone_obj.rotation_euler = (radians(0),radians(180),radians(0))
        stone_obj.location = (action_pos[0],action_pos[1],0.8)
        rotate_y = 180
    rotate_z = 0
    stone_obj.rotation_euler.x = radians(0)
    stone_obj.keyframe_insert(data_path="rotation_euler", index=0)  # X軸
    stone_obj.keyframe_insert(data_path="location", index=-1)
    stone_obj.keyframe_insert(data_path="rotation_euler", index=-1)
    bpy.context.scene.frame_set(next_start_F+141)
    #stone_obj.rotation_euler = (radians(0),stone_obj.rotation_euler[1]+radians(360),stone_obj.rotation_euler.z-radians(360))
    stone_obj.rotation_euler.y = radians(rotate_y+360)
    stone_obj.keyframe_insert(data_path="rotation_euler", index=1)  # Y軸
    stone_obj.rotation_euler.z = radians(rotate_z-360)
    stone_obj.keyframe_insert(data_path="rotation_euler", index=2)  # Z軸
    stone_obj.location = (action_pos[0],action_pos[1],0.18)
    stone_obj.keyframe_insert(data_path="location", index=-1)
    bpy.context.scene.frame_set(next_start_F+142)
    #stone_obj.rotation_euler = (radians(0),stone_obj.rotation_euler[1]+radians(360),stone_obj.rotation_euler.z-radians(360))
    stone_obj.rotation_euler.x = radians(0)
    stone_obj.keyframe_insert(data_path="rotation_euler", index=0)  # X軸
    stone_obj.rotation_euler.y = radians(rotate_y)
    stone_obj.keyframe_insert(data_path="rotation_euler", index=1)  # Y軸
    stone_obj.rotation_euler.z = radians(rotate_z)
    stone_obj.keyframe_insert(data_path="rotation_euler", index=2)  # Z軸
    stone_obj.location = (action_pos[0],action_pos[1],0.18)
    stone_obj.keyframe_insert(data_path="location", index=-1)
        #stone_obj.keyframe_insert(data_path="rotation_euler", index=-1)
    for flip in flips:
        flip_str = othello_play.convert_act_bit2str(flip)
        stone_obj_name = "stone_"+flip_str
        stone_obj = bpy.data.objects[stone_obj_name]
        """ bpy.context.scene.frame_set(next_start_F+133)
        if color==1:
            stone_obj.rotation_euler.x = radians(-180)
            stone_obj.rotation_euler.y =radians(0)
        else:
            stone_obj.rotation_euler.x = radians(0)
            stone_obj.rotation_euler.y = radians(0)
        stone_obj.keyframe_insert(data_path="rotation_euler", index=-1) """
        bpy.context.scene.frame_set(next_start_F+134)
        stone_obj.location.z = 0.18
        if color == 1:
            stone_obj.rotation_euler.y = radians(180)
            stone_obj.rotation_euler.x = radians(0)
            rotate_y = 180
        else:
            stone_obj.rotation_euler.y = radians(0)
            stone_obj.rotation_euler.x = radians(0)
            rotate_y = 0
        stone_obj.keyframe_insert(data_path="rotation_euler", index=-1)
        stone_obj.keyframe_insert(data_path="location", index=2)
        bpy.context.scene.frame_set(next_start_F+144)
        stone_obj.location.z = 0.36
        stone_obj.rotation_euler.y = radians(rotate_y -270)
        stone_obj.keyframe_insert(data_path="rotation_euler", index=1)
        stone_obj.keyframe_insert(data_path="location", index=2)
        bpy.context.scene.frame_set(next_start_F+153)
        stone_obj.location.z = 0.18
        stone_obj.rotation_euler.y = radians(rotate_y -540)
        stone_obj.keyframe_insert(data_path="rotation_euler", index=1)
        stone_obj.keyframe_insert(data_path="location", index=2)
        bpy.context.scene.frame_set(next_start_F+154)
        stone_obj.location.z = 0.18
        if color == -1:
            stone_obj.rotation_euler.y = radians(rotate_y -540+720)
        else:
            stone_obj.rotation_euler.y = radians(rotate_y -540+360)
        stone_obj.keyframe_insert(data_path="rotation_euler", index=1)
        stone_obj.keyframe_insert(data_path="location", index=2)


    next_start_F = next_start_F2
#print(text_settings)
bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.depsgraph_update_post.clear()
bpy.app.handlers.frame_change_pre.append(update_text)
#bpy.app.handlers.depsgraph_update_post.append(update_text)
bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(update_text)