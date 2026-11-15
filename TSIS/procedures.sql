-- 1. Процедура добавления телефона к существующему контакту
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    IF v_contact_id IS NOT NULL THEN
        INSERT INTO phones(contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
    ELSE
        RAISE EXCEPTION 'Контакт с именем % не найден', p_contact_name;
    END IF;
END;
$$;

-- 2. Процедура перемещения контакта в группу (создает группу, если её нет)
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- Автоматически создаем группу, если она еще не существует
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    -- Получаем ID группы
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    -- Обновляем группу контакта
    UPDATE contacts 
    SET group_id = v_group_id 
    WHERE name = p_contact_name;
END;
$$;

-- 3. Функция расширенного поиска (имя, email, телефоны, группа)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id INT, 
    contact_name VARCHAR, 
    contact_email VARCHAR, 
    contact_birthday DATE, 
    group_name VARCHAR, 
    phone_number VARCHAR, 
    phone_type VARCHAR
) AS $$
BEGIN
    RETURN QUERY 
    SELECT DISTINCT 
        c.id, 
        c.name, 
        c.email, 
        c.birthday, 
        g.name AS group_name, 
        p.phone, 
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;