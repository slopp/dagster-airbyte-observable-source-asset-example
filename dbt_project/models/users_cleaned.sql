{{
        config(
                dagster_auto_materialize_policy={"type":"eager"}
        )
}}
select
        user_id, 
        username as user_name
from {{ source('postgres_replica', 'users') }}