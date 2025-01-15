'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-15 13:37:52
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-15 13:44:43
FilePath: \autoAccountor\tools\init_price.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os

customer_prices = {
    '小球': {},
    '大球2.5': {},
    '大球3.2': {}
}

def initialize_customer_prices():
    """Initialize default prices for all customers."""
    try:
        # Get all customer files
        customer_files = [f for f in os.listdir('customers') if f.endswith('.txt')]
        customer_names = [os.path.splitext(f)[0] for f in customer_files]
        
        # Default prices
        default_prices = {
            '小球': 100,
            '大球2.5': 200,
            '大球3.2': 300
        }
        
        # Create pricing data
        pricing_data = []
        for customer in customer_names:
            pricing_data.append(f"客户: {customer}")
            for product, price in default_prices.items():
                pricing_data.append(f"    {product}: {price}元")
            pricing_data.append("")  # Empty line between customers
            
            # Update customer_prices dictionary
            customer_prices['小球'][customer] = default_prices['小球']
            customer_prices['大球2.5'][customer] = default_prices['大球2.5']
            customer_prices['大球3.2'][customer] = default_prices['大球3.2']
            
        # Write to price file
        with open('info/价格.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(pricing_data))
            
    except Exception as e:
        print(f"\033[91mError initializing prices: {e}\033[0m")

# Call the function to initialize prices
initialize_customer_prices()