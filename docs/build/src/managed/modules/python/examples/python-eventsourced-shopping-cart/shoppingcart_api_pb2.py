# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: shoppingcart_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from akkaserverless.akkaserverless import annotations_pb2 as akkaserverless_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='shoppingcart_api.proto',
  package='com.example.shoppingcart',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16shoppingcart_api.proto\x12\x18\x63om.example.shoppingcart\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a akkaserverless/annotations.proto\"Y\n\x0b\x41\x64\x64LineItem\x12\x16\n\x07\x63\x61rt_id\x18\x01 \x01(\tB\x05\xc2\x43\x02\x08\x01\x12\x12\n\nproduct_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x10\n\x08quantity\x18\x04 \x01(\x05\"<\n\x0eRemoveLineItem\x12\x16\n\x07\x63\x61rt_id\x18\x01 \x01(\tB\x05\xc2\x43\x02\x08\x01\x12\x12\n\nproduct_id\x18\x02 \x01(\t\")\n\x0fGetShoppingCart\x12\x16\n\x07\x63\x61rt_id\x18\x01 \x01(\tB\x05\xc2\x43\x02\x08\x01\">\n\x08LineItem\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\x03 \x01(\x05\"9\n\x04\x43\x61rt\x12\x31\n\x05items\x18\x01 \x03(\x0b\x32\".com.example.shoppingcart.LineItem2\xb8\x03\n\x13ShoppingCartService\x12n\n\x07\x41\x64\x64Item\x12%.com.example.shoppingcart.AddLineItem\x1a\x16.google.protobuf.Empty\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/cart/{cart_id}/items/add:\x01*\x12\x81\x01\n\nRemoveItem\x12(.com.example.shoppingcart.RemoveLineItem\x1a\x16.google.protobuf.Empty\"1\x82\xd3\xe4\x93\x02+\")/cart/{cart_id}/items/{product_id}/remove\x12\x8f\x01\n\x07GetCart\x12).com.example.shoppingcart.GetShoppingCart\x1a\x1e.com.example.shoppingcart.Cart\"9\x82\xd3\xe4\x93\x02\x33\x12\x10/carts/{cart_id}Z\x1f\x12\x16/carts/{cart_id}/itemsb\x05items\x1a\x1b\xc2\x43\x18\x08\x02\x12\x14.domain.ShoppingCartb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,akkaserverless_dot_annotations__pb2.DESCRIPTOR,])




_ADDLINEITEM = _descriptor.Descriptor(
  name='AddLineItem',
  full_name='com.example.shoppingcart.AddLineItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cart_id', full_name='com.example.shoppingcart.AddLineItem.cart_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\302C\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='product_id', full_name='com.example.shoppingcart.AddLineItem.product_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='com.example.shoppingcart.AddLineItem.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quantity', full_name='com.example.shoppingcart.AddLineItem.quantity', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=234,
)


_REMOVELINEITEM = _descriptor.Descriptor(
  name='RemoveLineItem',
  full_name='com.example.shoppingcart.RemoveLineItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cart_id', full_name='com.example.shoppingcart.RemoveLineItem.cart_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\302C\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='product_id', full_name='com.example.shoppingcart.RemoveLineItem.product_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=236,
  serialized_end=296,
)


_GETSHOPPINGCART = _descriptor.Descriptor(
  name='GetShoppingCart',
  full_name='com.example.shoppingcart.GetShoppingCart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cart_id', full_name='com.example.shoppingcart.GetShoppingCart.cart_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\302C\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=298,
  serialized_end=339,
)


_LINEITEM = _descriptor.Descriptor(
  name='LineItem',
  full_name='com.example.shoppingcart.LineItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_id', full_name='com.example.shoppingcart.LineItem.product_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='com.example.shoppingcart.LineItem.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quantity', full_name='com.example.shoppingcart.LineItem.quantity', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=341,
  serialized_end=403,
)


_CART = _descriptor.Descriptor(
  name='Cart',
  full_name='com.example.shoppingcart.Cart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='items', full_name='com.example.shoppingcart.Cart.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=405,
  serialized_end=462,
)

_CART.fields_by_name['items'].message_type = _LINEITEM
DESCRIPTOR.message_types_by_name['AddLineItem'] = _ADDLINEITEM
DESCRIPTOR.message_types_by_name['RemoveLineItem'] = _REMOVELINEITEM
DESCRIPTOR.message_types_by_name['GetShoppingCart'] = _GETSHOPPINGCART
DESCRIPTOR.message_types_by_name['LineItem'] = _LINEITEM
DESCRIPTOR.message_types_by_name['Cart'] = _CART
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AddLineItem = _reflection.GeneratedProtocolMessageType('AddLineItem', (_message.Message,), {
  'DESCRIPTOR' : _ADDLINEITEM,
  '__module__' : 'shoppingcart_api_pb2'
  # @@protoc_insertion_point(class_scope:com.example.shoppingcart.AddLineItem)
  })
_sym_db.RegisterMessage(AddLineItem)

RemoveLineItem = _reflection.GeneratedProtocolMessageType('RemoveLineItem', (_message.Message,), {
  'DESCRIPTOR' : _REMOVELINEITEM,
  '__module__' : 'shoppingcart_api_pb2'
  # @@protoc_insertion_point(class_scope:com.example.shoppingcart.RemoveLineItem)
  })
_sym_db.RegisterMessage(RemoveLineItem)

GetShoppingCart = _reflection.GeneratedProtocolMessageType('GetShoppingCart', (_message.Message,), {
  'DESCRIPTOR' : _GETSHOPPINGCART,
  '__module__' : 'shoppingcart_api_pb2'
  # @@protoc_insertion_point(class_scope:com.example.shoppingcart.GetShoppingCart)
  })
_sym_db.RegisterMessage(GetShoppingCart)

LineItem = _reflection.GeneratedProtocolMessageType('LineItem', (_message.Message,), {
  'DESCRIPTOR' : _LINEITEM,
  '__module__' : 'shoppingcart_api_pb2'
  # @@protoc_insertion_point(class_scope:com.example.shoppingcart.LineItem)
  })
_sym_db.RegisterMessage(LineItem)

Cart = _reflection.GeneratedProtocolMessageType('Cart', (_message.Message,), {
  'DESCRIPTOR' : _CART,
  '__module__' : 'shoppingcart_api_pb2'
  # @@protoc_insertion_point(class_scope:com.example.shoppingcart.Cart)
  })
_sym_db.RegisterMessage(Cart)


_ADDLINEITEM.fields_by_name['cart_id']._options = None
_REMOVELINEITEM.fields_by_name['cart_id']._options = None
_GETSHOPPINGCART.fields_by_name['cart_id']._options = None

_SHOPPINGCARTSERVICE = _descriptor.ServiceDescriptor(
  name='ShoppingCartService',
  full_name='com.example.shoppingcart.ShoppingCartService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=b'\302C\030\010\002\022\024.domain.ShoppingCart',
  create_key=_descriptor._internal_create_key,
  serialized_start=465,
  serialized_end=905,
  methods=[
  _descriptor.MethodDescriptor(
    name='AddItem',
    full_name='com.example.shoppingcart.ShoppingCartService.AddItem',
    index=0,
    containing_service=None,
    input_type=_ADDLINEITEM,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002\036\"\031/cart/{cart_id}/items/add:\001*',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RemoveItem',
    full_name='com.example.shoppingcart.ShoppingCartService.RemoveItem',
    index=1,
    containing_service=None,
    input_type=_REMOVELINEITEM,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002+\")/cart/{cart_id}/items/{product_id}/remove',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCart',
    full_name='com.example.shoppingcart.ShoppingCartService.GetCart',
    index=2,
    containing_service=None,
    input_type=_GETSHOPPINGCART,
    output_type=_CART,
    serialized_options=b'\202\323\344\223\0023\022\020/carts/{cart_id}Z\037\022\026/carts/{cart_id}/itemsb\005items',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SHOPPINGCARTSERVICE)

DESCRIPTOR.services_by_name['ShoppingCartService'] = _SHOPPINGCARTSERVICE

# @@protoc_insertion_point(module_scope)
