package dev.heinisch.template.endpoint;

import dev.heinisch.template.api.dto.MessageDto;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.processing.Generated;
import org.openapitools.model.MessageResponse;
import org.openapitools.model.PaginatedMessageResponse;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2025-02-28T19:18:30+0800",
    comments = "version: 1.6.2, compiler: javac, environment: Java 21.0.3 (Oracle Corporation)"
)
@Component
public class RestEntitiesMapperImpl implements RestEntitiesMapper {

    @Override
    public MessageResponse dtoToResponseObject(MessageDto dto) {
        if ( dto == null ) {
            return null;
        }

        MessageResponse messageResponse = new MessageResponse();

        messageResponse.setText( dto.getText() );
        messageResponse.setId( dto.getId() );

        return messageResponse;
    }

    @Override
    public PaginatedMessageResponse dtoToResponseObject(Page<MessageDto> dto) {
        if ( dto == null ) {
            return null;
        }

        PaginatedMessageResponse paginatedMessageResponse = new PaginatedMessageResponse();

        paginatedMessageResponse.setTotalElements( dto.getTotalElements() );
        paginatedMessageResponse.setTotalPages( dto.getTotalPages() );
        paginatedMessageResponse.setFirst( dto.isFirst() );
        paginatedMessageResponse.setLast( dto.isLast() );
        paginatedMessageResponse.setNumber( dto.getNumber() );
        paginatedMessageResponse.setNumberOfElements( dto.getNumberOfElements() );
        paginatedMessageResponse.setSize( dto.getSize() );
        paginatedMessageResponse.setEmpty( dto.isEmpty() );
        if ( dto.hasContent() ) {
            paginatedMessageResponse.setContent( messageDtoListToMessageResponseList( dto.getContent() ) );
        }

        return paginatedMessageResponse;
    }

    protected List<MessageResponse> messageDtoListToMessageResponseList(List<MessageDto> list) {
        if ( list == null ) {
            return null;
        }

        List<MessageResponse> list1 = new ArrayList<MessageResponse>( list.size() );
        for ( MessageDto messageDto : list ) {
            list1.add( dtoToResponseObject( messageDto ) );
        }

        return list1;
    }
}
