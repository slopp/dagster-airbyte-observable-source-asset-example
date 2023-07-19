select
        date_trunc('d', oc.order_time::timestamp) as order_date,
        ua.user_name as user,
        sum(oc.order_value) as total_value,
        count(*) as num_orders
from
        {{ ref("orders_cleaned") }} oc
        join
        {{ ref("users_cleaned") }} ua
        on oc.user_id = ua.user_id
group by 1, 2 order by 1
