alter table tokens add constraint tokens_pk primary key (address, epoch_number);

create index tokens_epoch_number_index on tokens (epoch_number desc);
