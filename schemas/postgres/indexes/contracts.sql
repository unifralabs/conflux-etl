alter table contracts add constraint contracts_pk primary key (address, epoch_number);

create index contracts_epoch_number_index on contracts (epoch_number desc);
create index contracts_is_erc20_index on contracts (is_erc20, epoch_number desc);
create index contracts_is_erc721_index on contracts (is_erc721, epoch_number desc);
