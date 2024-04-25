import csv
import os
import pandas as pd
from flask import Blueprint, render_template, redirect, request, jsonify, url_for, session, current_app, flash, render_template_string

historyloggor = Blueprint('historyloggor', __name__, url_prefix='/events')


# 使用数据库


@historyloggor.route('/')
def show_table():
    page = request.args.get('page', 1, type=int)  # 从查询参数获取当前页数
    per_page = 20  # 每页显示的记录数量
    data_path = './data/historyloggerdata.csv'  # 数据文件路径
    data = pd.read_csv(data_path)

    # 计算总页数
    total_pages = (len(data) + per_page - 1) // per_page

    # 获取当前页的数据
    start = (page - 1) * per_page
    end = start + per_page
    page_data = data.iloc[start:end]

    # 将DataFrame转换为字典列表，方便在Jinja2中迭代
    records = page_data.to_dict(orient='records')

    return render_template('lyear_pages_doc.html', records=records, current_page=page, total_pages=total_pages)


@historyloggor.route('/delete-record', methods=['POST'])
def delete_record():

    try:
        record_id = request.form['id']
        data_path = './data/historyloggerdata.csv'
        data = pd.read_csv(data_path)

        # 删除指定的记录
        data['编号'] = data['编号'].astype(str)
        data = data[data['编号'] != record_id]
        data.to_csv(data_path, index=False)  # 保存更新后的CSV文件

        return jsonify({'success': True})
        # return jsonify({'key': 'value'})
    except Exception as e:
        # return jsonify({'error': str(e)}), 500
        return jsonify({'success': False, 'message': '删除操作失败'}), 500


# @historyloggor.route('/delete', methods=['POST'])
# def delete_records():
#     data = request.get_json()
#     ids_to_delete = data['ids']
#     file_path = './data/historyloggerdata.csv'
#
#     # 读取CSV文件
#     df = pd.read_csv(file_path)
#
#     # 删除指定的行
#     df = df[~df['编号'].isin(ids_to_delete)]
#
#     # 保存回CSV文件
#     df.to_csv(file_path, index=False)
#
#     return jsonify({'status': 'success', 'deleted_ids': ids_to_delete})


@historyloggor.route('/update', methods=['get', 'POST'])
def update_record():
    try:
        # 尝试解析 JSON 数据
        data = request.get_json()
        # print("Received data:", data)  # 调试输出
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400

        # 检查所有必需字段是否存在
        required_fields = ['id', 'date', 'analysisType', 'analysisResult', 'oodType', 'remarks']
        if any(field not in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        # 尝试读取CSV文件
        df = pd.read_csv('./data/historyloggerdata.csv')


        # 更新数据
        index = df[df['编号'] == int(data['id'])].index





        if index.empty:
            return jsonify({'status': 'error', 'message': 'Record not found'}), 404

        # for field in ['日期', '分析类型', '分析结果', 'ood类型', '备注']:
        #     df.loc[index, field] = data[field.lower()]

        field_mapping = {'date': '日期', 'analysisType': '分析类型', 'analysisResult': '分析结果', 'oodType': 'ood类型',
                         'remarks': '备注'}
        for field in field_mapping:
            if field in data:
                df.loc[index, field_mapping[field]] = data[field]

        # 保存修改后的数据
        df.to_csv('./data/historyloggerdata.csv', index=False)

        return jsonify({'status': 'success', 'message': 'Record updated'})

    except Exception as e:
        # 通用错误处理
        print("Error:", e)  # 输出错误信息
        return jsonify({'status': 'error', 'message': str(e)}), 500


# def truncate(string, length=20, ellipsis=True):
#     if len(string) > length:
#         return string[:length] + ('...' if ellipsis else '')
#     return string





