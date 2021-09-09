# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import shoppingcart_api_pb2 as shoppingcart__api__pb2


class ShoppingCartServiceStub(object):
    """tag::proto_service[]
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddItem = channel.unary_unary(
                '/com.example.shoppingcart.ShoppingCartService/AddItem',
                request_serializer=shoppingcart__api__pb2.AddLineItem.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.RemoveItem = channel.unary_unary(
                '/com.example.shoppingcart.ShoppingCartService/RemoveItem',
                request_serializer=shoppingcart__api__pb2.RemoveLineItem.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetCart = channel.unary_unary(
                '/com.example.shoppingcart.ShoppingCartService/GetCart',
                request_serializer=shoppingcart__api__pb2.GetShoppingCart.SerializeToString,
                response_deserializer=shoppingcart__api__pb2.Cart.FromString,
                )
        self.RemoveCart = channel.unary_unary(
                '/com.example.shoppingcart.ShoppingCartService/RemoveCart',
                request_serializer=shoppingcart__api__pb2.RemoveShoppingCart.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class ShoppingCartServiceServicer(object):
    """tag::proto_service[]
    """

    def AddItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveCart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ShoppingCartServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddItem': grpc.unary_unary_rpc_method_handler(
                    servicer.AddItem,
                    request_deserializer=shoppingcart__api__pb2.AddLineItem.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'RemoveItem': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveItem,
                    request_deserializer=shoppingcart__api__pb2.RemoveLineItem.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetCart': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCart,
                    request_deserializer=shoppingcart__api__pb2.GetShoppingCart.FromString,
                    response_serializer=shoppingcart__api__pb2.Cart.SerializeToString,
            ),
            'RemoveCart': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveCart,
                    request_deserializer=shoppingcart__api__pb2.RemoveShoppingCart.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.example.shoppingcart.ShoppingCartService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ShoppingCartService(object):
    """tag::proto_service[]
    """

    @staticmethod
    def AddItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.example.shoppingcart.ShoppingCartService/AddItem',
            shoppingcart__api__pb2.AddLineItem.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.example.shoppingcart.ShoppingCartService/RemoveItem',
            shoppingcart__api__pb2.RemoveLineItem.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.example.shoppingcart.ShoppingCartService/GetCart',
            shoppingcart__api__pb2.GetShoppingCart.SerializeToString,
            shoppingcart__api__pb2.Cart.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveCart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.example.shoppingcart.ShoppingCartService/RemoveCart',
            shoppingcart__api__pb2.RemoveShoppingCart.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
