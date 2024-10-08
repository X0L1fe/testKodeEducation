PGDMP                      |            KodeEducation    16.4    16.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16450    KodeEducation    DATABASE     �   CREATE DATABASE "KodeEducation" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "KodeEducation";
                postgres    false            �            1259    16463    notes    TABLE     �   CREATE TABLE public.notes (
    id integer NOT NULL,
    title character varying(255),
    content text,
    owner_id integer
);
    DROP TABLE public.notes;
       public         heap    postgres    false            �            1259    16462    notes_id_seq    SEQUENCE     �   CREATE SEQUENCE public.notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.notes_id_seq;
       public          postgres    false    218            �           0    0    notes_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.notes_id_seq OWNED BY public.notes.id;
          public          postgres    false    217            �            1259    16452    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    hashed_password character varying(255) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16451    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    216            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    215                        2604    16466    notes id    DEFAULT     d   ALTER TABLE ONLY public.notes ALTER COLUMN id SET DEFAULT nextval('public.notes_id_seq'::regclass);
 7   ALTER TABLE public.notes ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218                       2604    16455    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216            �          0    16463    notes 
   TABLE DATA           =   COPY public.notes (id, title, content, owner_id) FROM stdin;
    public          postgres    false    218   <       �          0    16452    users 
   TABLE DATA           >   COPY public.users (id, username, hashed_password) FROM stdin;
    public          postgres    false    216   �       �           0    0    notes_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.notes_id_seq', 38, true);
          public          postgres    false    217            �           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 11, true);
          public          postgres    false    215            &           2606    16470    notes notes_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.notes DROP CONSTRAINT notes_pkey;
       public            postgres    false    218            "           2606    16459    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    216            $           2606    16461    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    216            '           2606    16471    notes notes_owner_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.notes DROP CONSTRAINT notes_owner_id_fkey;
       public          postgres    false    216    218    4642            �   �  x��R�N�@��_�����(�EJ����)���P"�� 
((qVL�/���g�I HH��nnwvnv}ÏleD�Ź�y���@�3�?s�3�%Y�Y��+j��bo�/�#�5NC c��	�HZ#乤�D�s�{A�hRr���I���z�Y�+2��H���4�x����P���UE�+.鎊Or�(q ^�b+Du7��r��ȩ��=t�%v�Ű*�ڌ�`m���w%;�X�ծ���s�Ŧ@\�R��8��-��w톓���F�Q���ڎ_�_=V���Etڍ:�uq�#|m���4zM�9�Q'��S����
|X��
�;���æ��ʜ�t��EW����N���r��Ύ�!����'��{���.�X      �   �   x�5�Kr�0  �59�`R>�%LDm�( �����BHU<����yȐ��(Tǥ0L\���Y��|gQw�!��H��G�,UV��z���Rķ:�>?�`#�m6O��q�i��oy�9P��Rr���^��﫿��^��	��(Z��uzCW=-���{�)�P�m"���xq,fdʳ�W�x�c:�� ��?E}     