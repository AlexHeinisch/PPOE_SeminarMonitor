package org.openapitools.model;

import java.net.URI;
import java.util.Objects;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import org.springframework.lang.Nullable;
import org.openapitools.jackson.nullable.JsonNullable;
import java.time.OffsetDateTime;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import io.swagger.v3.oas.annotations.media.Schema;


import java.util.*;
import jakarta.annotation.Generated;

/**
 * MessageResponse
 */

@Generated(value = "org.openapitools.codegen.languages.SpringCodegen", date = "2025-02-28T19:18:29.784073+08:00[Asia/Taipei]", comments = "Generator version: 7.11.0")
public class MessageResponse {

  private String text;

  private @Nullable Long id;

  public MessageResponse() {
    super();
  }

  /**
   * Constructor with only required parameters
   */
  public MessageResponse(String text) {
    this.text = text;
  }

  public MessageResponse text(String text) {
    this.text = text;
    return this;
  }

  /**
   * Get text
   * @return text
   */
  @NotNull @Size(min = 5, max = 10) 
  @Schema(name = "text", requiredMode = Schema.RequiredMode.REQUIRED)
  @JsonProperty("text")
  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }

  public MessageResponse id(Long id) {
    this.id = id;
    return this;
  }

  /**
   * Get id
   * @return id
   */
  
  @Schema(name = "id", requiredMode = Schema.RequiredMode.NOT_REQUIRED)
  @JsonProperty("id")
  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    MessageResponse messageResponse = (MessageResponse) o;
    return Objects.equals(this.text, messageResponse.text) &&
        Objects.equals(this.id, messageResponse.id);
  }

  @Override
  public int hashCode() {
    return Objects.hash(text, id);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class MessageResponse {\n");
    sb.append("    text: ").append(toIndentedString(text)).append("\n");
    sb.append("    id: ").append(toIndentedString(id)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }
}

