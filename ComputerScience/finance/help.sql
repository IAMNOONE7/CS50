/*Create table if not exists holdings
(
    user_id integer not null,
    symbol text not null,
    shares integer not null check (shares >=0),
    primary key (user_id, symbol)
);

create table if not exists transactions
(
    id integer primary key autoincrement,
    user_id integer not null,
    symbol text not null,
    shares integer not null,
    price numeric not null,
    ts datetime default CURRENT_TIMESTAMP
);
*/


