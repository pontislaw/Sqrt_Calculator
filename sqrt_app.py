import streamlit as st

def sqrt_estimate(n, decimals=3, verbose=True):
    """
    手動估算平方根（可指定小數位數，不用內建函數）
    :param n: 要開平方的正整數
    :param decimals: 小數點後要保留幾位（預設 3）
    :param verbose: 是否印出詳細過程（預設 True）
    :return: 估算結果（浮點數，保留指定小數位）
    """
    if n < 0:
        raise ValueError("請輸入非負整數")
    if n == 0:
        if verbose:
            st.write(f"\n📌 最終平方根估值（{decimals} 位小數）：0." + "0" * decimals)
        return 0.0

    if verbose:
        st.write(f"\n🔢 輸入的數字為：{n}")

    # 計算位數
    digits = 0
    temp = n
    while temp > 0:
        temp //= 10
        digits += 1
    root_digits = digits // 2 if digits % 2 == 0 else (digits // 2) + 1

    if verbose:
        st.write(f"🧮 預估平方根應為 {root_digits} 位數")

    # 最大可能平方根 = 10^root_digits - 1
    max_root = 10 ** root_digits - 1
    if verbose:
        st.write(f"🎯 從最大可能平方根 {max_root} 開始分層估算")

    # 分層估算整數部分
    result = 0
    place_value = 10 ** (root_digits - 1)
    while place_value >= 1:
        for digit in range(9, -1, -1):
            trial = result + digit * place_value
            if trial * trial <= n:
                result = trial
                break
        place_value //= 10

    x = result
    if verbose:
        st.write(f"\n✅ 找到整數平方根為：{x}，因為 {x}² = {x*x} <= {n}")

    if x * x == n:
        if verbose:
            st.write(f"\n📌 最終平方根估值（{decimals} 位小數）：{x}." + "0" * decimals)
        return float(f"{x}.", + "0" * decimals)

    # 小數估算（根據 decimals 決定幾位）
    place = 0.1
    for _ in range(decimals):
        for d in range(9, -1, -1):
            trial = result + d * place
            if trial * trial <= n:
                result = trial
                break
        place /= 10

    # 四捨五入
    round_factor = 10 ** (decimals + 1)
    multiplied = int(result * round_factor)
    last_digit = multiplied % 10
    multiplied //= 10
    if last_digit >= 5:
        multiplied += 1
    final_result = multiplied / (10 ** decimals)

    if verbose:
        st.write(f"\n📌 最終平方根估值（{decimals} 位小數）：{final_result:.{decimals}f}")

    return final_result

# Streamlit 介面
st.title("🧮 平方根估算器（不使用函數）")

n = st.number_input("請輸入要開平方的正整數：", min_value=0, step=1)
decimals = st.slider("要保留幾位小數？", min_value=0, max_value=6, value=3)

if st.button("估算平方根"):
    try:
        result = sqrt_estimate(int(n), decimals=decimals, verbose=True)
    except ValueError as e:
        st.error(str(e))
