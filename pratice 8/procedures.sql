CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(names VARCHAR[], phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    curr_name VARCHAR;
    curr_phone VARCHAR;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        curr_name := names[i];
        curr_phone := phones[i];
        
        -- Простейшая валидация: если телефон короче 5 символов — пропускаем / выводим уведомление
        IF length(curr_phone) < 5 THEN
            RAISE NOTICE 'Некорректный номер у контакта: %, телефон: %', curr_name, curr_phone;
        ELSE
            -- Делаем вставку или обновление
            INSERT INTO contacts(name, phone) VALUES(curr_name, curr_phone)
            ON CONFLICT DO NOTHING;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_query VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_query OR phone = p_query;
END;
$$;