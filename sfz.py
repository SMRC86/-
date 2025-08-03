import datetime
from collections import OrderedDict

# 加载行政区划代码库
def load_region_data(file_path='region_codes.txt'):
    """
    从指定路径的 txt 文件加载行政区划数据
    :param file_path: 行政区划数据文件路径，默认为 'region_codes.txt'
    :return: 包含行政区划代码和对应名称的字典
    """
    region_codes = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    region_codes[parts[0]] = parts[1]
    except FileNotFoundError:
        print(f"错误：找不到行政区划数据文件 {file_path}")
    return region_codes

# 获取地区详细信息
def get_region_detail(code, region_codes):
    """
    根据行政区划代码递归解析行政区划
    :param code: 行政区划代码
    :param region_codes: 行政区划代码库字典
    :return: 包含省、市、区信息的列表
    """
    details = []
    # 省级 (前 2 位补 4 个 0)
    province_code = code[:2] + "0000"
    province = region_codes.get(province_code)
    if province:
        details.append(province)
    else:
        return ["未知省份"]

    # 市级 (前 4 位补 2 个 0)
    city_code = code[:4] + "00"
    if city_code != province_code:
        city = region_codes.get(city_code)
        if city:
            details.append(city.split('/')[-1])

    # 区县级 (完整 6 位)
    district = region_codes.get(code)
    if district:
        details.append(district.split('/')[-1])

    return details if details else ["未知地区"]

# 计算身份证校验码
def compute_check_code(id_17):
    """
    计算 17 位身份证号码的校验码
    :param id_17: 17 位身份证号码
    :return: 校验码
    """
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    total = sum(int(id_17[i]) * coefficients[i] for i in range(17))
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    return check_codes[total % 11]

# 将 15 位身份证升级为 18 位
def upgrade_15_to_18(id_15):
    """
    将 15 位身份证号码升级为 18 位
    :param id_15: 15 位身份证号码
    :return: 18 位身份证号码或 None（如果输入无效）
    """
    if len(id_15) == 15 and id_15.isdigit():
        new_id = id_15[:6] + "19" + id_15[6:]
        return new_id + compute_check_code(new_id)
    return None

# 根据出生日期计算星座
def get_zodiac_sign(birth_date):
    """
    根据出生日期计算星座
    :param birth_date: 出生日期（datetime.date 对象）
    :return: 星座名称
    """
    month = birth_date.month
    day = birth_date.day
    zodiac_signs = [
        (120, '水瓶座'), (219, '双鱼座'), (321, '白羊座'), (420, '金牛座'),
        (521, '双子座'), (622, '巨蟹座'), (723, '狮子座'), (823, '处女座'),
        (923, '天秤座'), (1024, '天蝎座'), (1123, '射手座'), (1222, '摩羯座')
    ]
    birth_num = int(f"{month}{day:02d}")
    for index, (cutoff, sign) in enumerate(zodiac_signs):
        if birth_num < cutoff:
            return zodiac_signs[index - 1][1] if index > 0 else zodiac_signs[-1][1]
    return zodiac_signs[-1][1]

# 根据出生年份计算生肖
def get_chinese_zodiac(year):
    """
    根据出生年份计算生肖
    :param year: 出生年份
    :return: 生肖名称
    """
    zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    base_year = 1900
    index = (year - base_year) % 12
    return zodiacs[index]

# 根据出生日期计算出生季节
def get_birth_season(birth_date):
    """
    根据出生日期计算出生季节
    :param birth_date: 出生日期（datetime.date 对象）
    :return: 季节名称
    """
    month = birth_date.month
    if 3 <= month <= 5:
        return "春季"
    elif 6 <= month <= 8:
        return "夏季"
    elif 9 <= month <= 11:
        return "秋季"
    else:
        return "冬季"

# 解析身份证详细信息
def parse_id_info(id_number, region_codes):
    """
    解析身份证号码的详细信息
    :param id_number: 身份证号码
    :param region_codes: 行政区划代码库字典
    :return: 包含身份证详细信息的有序字典
    """
    info = OrderedDict([
        ("地址", "未知"),
        ("出生日期", ""),
        ("年龄", 0),
        ("性别", ""),
        ("校验码", ""),
        ("有效性", False),
        ("错误信息", ""),
        ("星座", ""),
        ("生肖", ""),
        ("出生季节", "")
    ])

    id_num = id_number.strip().upper()
    current_date = datetime.date.today()

    # 处理 17 位身份证
    if len(id_num) == 17:
        if id_num.isdigit():
            check_code = compute_check_code(id_num)
            id_num = id_num + check_code
            print(f"计算得到的完整 18 位身份证号码为: {id_num}")
        else:
            info["错误信息"] = "错误：17 位身份证必须全为数字"
            return info

    # 验证基本格式
    if len(id_num) not in (15, 18):
        info["错误信息"] = "错误：身份证号码长度不正确"
        return info

    # 处理 15 位身份证
    if len(id_num) == 15:
        id_num = upgrade_15_to_18(id_num)
        if not id_num:
            info["错误信息"] = "错误：无效的 15 位身份证号码"
            return info

    # 验证 18 位格式
    if len(id_num) != 18 or not id_num[:17].isdigit():
        info["错误信息"] = "错误：无效的 18 位身份证格式"
        return info

    # 验证校验码
    expected_check = compute_check_code(id_num[:17])
    if id_num[17] != expected_check:
        info["错误信息"] = f"错误：校验码不匹配（应为{expected_check}）"
        return info

    # 解析地址信息
    region_code = id_num[:6]
    region_details = get_region_detail(region_code, region_codes)
    info["地址"] = " ".join(region_details)

    # 解析出生日期
    try:
        birth_date = datetime.datetime.strptime(id_num[6:14], "%Y%m%d").date()
        info["年龄"] = current_date.year - birth_date.year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day)
        )
        info["出生日期"] = birth_date.strftime("%Y-%m-%d")
        info["星座"] = get_zodiac_sign(birth_date)
        info["生肖"] = get_chinese_zodiac(birth_date.year)
        info["出生季节"] = get_birth_season(birth_date)
    except ValueError:
        info["错误信息"] = "错误：无效的出生日期"
        return info

    # 解析性别
    gender_code = int(id_num[16])
    info["性别"] = "男" if gender_code % 2 == 1 else "女"
    info["校验码"] = id_num[17]
    info["有效性"] = True
    return info

# 主函数
def main():
    print("欢迎使用身份证信息解析系统！以下是本系统提供的功能：")
    print("1. 基本信息解析：")
    print("   - 地址信息：根据身份证前六位行政区划代码，查询对应的省、市、区信息。")
    print("   - 出生日期：从身份证号码中提取并格式化展示出生日期。")
    print("   - 年龄计算：依据当前日期和出生日期，精确计算周岁年龄。")
    print("   - 性别判断：通过身份证第 17 位数字判断性别。")
    print("   - 校验码验证：计算并验证身份证第 18 位校验码的正确性。")
    print("2. 特殊格式处理：")
    print("   - 15 位身份证升级：将 15 位身份证号码升级为 18 位。")
    print("   - 17 位号码计算：为 17 位身份证号码计算第 18 位校验码。")
    print("3. 隐藏信息挖掘：")
    print("   - 星座信息：根据出生日期确定对应的星座。")
    print("   - 生肖信息：根据出生年份确定对应的生肖。")
    print("   - 出生季节：根据出生日期判断出生季节。")
    print("4. 用户交互与错误处理：")
    print("   - 交互式操作：可多次输入身份证号码进行解析，输入 'q' 退出系统。")
    print("   - 错误提示：遇到问题时，给出详细的错误信息。")
    print("=" * 80)

    region_codes = load_region_data()
    print("身份证信息解析系统（含行政区划）")
    print("=" * 40)
    while True:
        id_input = input("\n请输入身份证号码（输入 q 退出）: ").strip()
        if id_input.lower() == 'q':
            break

        result = parse_id_info(id_input, region_codes)

        if result["有效性"]:
            print("\n[有效身份证信息]")
            for key, value in result.items():
                if key != "有效性":
                    print(f"• {key}：{value}")
        else:
            print("\n[无效身份证]")
            print(f"• 错误原因：{result['错误信息']}")
        print("=" * 40)

if __name__ == "__main__":
    main()
